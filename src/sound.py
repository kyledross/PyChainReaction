import functools
import numpy as np
import pygame

def apply_fade(audio_array, fade_duration, sample_rate):
    """
       Apply fade-in and fade-out effects to an audio array.

       :param audio_array: The numpy array representing the waveform.
       :param fade_duration: Duration of the fade-in and fade-out in seconds.
       :param sample_rate: The sampling rate of the waveform in Hz.
       :return: The audio array with fade-in and fade-out applied.
       """
    fade_samples = int(fade_duration * sample_rate)
    # Create fade-in and fade-out envelopes
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    # Apply fade-in
    audio_array[:fade_samples] *= fade_in
    # Apply fade-out
    audio_array[-fade_samples:] *= fade_out

    return audio_array

@functools.lru_cache(maxsize=50)
def generate_sweep_sound(start_frequency, end_frequency, sound_duration):
    """
    Generates a smooth frequency sweep from start_frequency to end_frequency.

    :param start_frequency: The starting frequency in Hertz (Hz).
    :param end_frequency: The ending frequency in Hertz (Hz).
    :param sound_duration: The duration of the sweep in seconds.
    :return: A pygame Sound object of the sweep.
    """
    sample_rate = 44100
    sound_duration = round(sound_duration * sample_rate) / sample_rate
    t = np.linspace(0, sound_duration, int(sample_rate * sound_duration), endpoint=False)

    # Use a smooth interpolation for frequency (logarithmic chirp is smoother than linear)
    frequencies = np.logspace(np.log10(start_frequency), np.log10(end_frequency), num=len(t))

    # Create the waveform for the frequency sweep
    waveform = 0.5 * np.sin(2 * np.pi * frequencies * t)

    # Add 2nd and 3rd harmonics
    waveform += 0.5 * np.sin(2 * np.pi * 2 * frequencies * t)  # 2nd harmonic
    waveform += 0.25 * np.sin(2 * np.pi * 3 * frequencies * t)  # 3rd harmonic
    waveform = apply_fade(waveform, fade_duration=0.1, sample_rate=sample_rate)

    # Ensure starts and ends near zero
    if waveform[0] != 0:
        waveform[0] = 0
    if waveform[-1] != 0:
        waveform[-1] = 0

    # Add short silence padding to the waveform
    padding_duration = 0.05  # 20 milliseconds of silence
    padding_samples = int(sample_rate * padding_duration)
    silence = np.zeros(padding_samples)

    # Concatenate silence to start and end
    waveform = np.concatenate([silence, waveform, silence])

    # normalize to prevent clipping
    waveform /= np.max(np.abs(waveform))  # Normalize to range [-1, 1]



    # apply fade
    waveform = apply_fade(
        waveform,
        fade_duration=0.1,
        sample_rate=sample_rate)

    # Convert the waveform to stereo
    stereo_wave = np.vstack((waveform, waveform)).T

    # Convert the waveform to a format suitable for pygame
    sound = pygame.sndarray.make_sound((32767 * stereo_wave).astype(np.int16).copy())
    return sound


def play_sweep(start_frequency, end_frequency, sound_duration, volume=0.1):
    """
    Plays a frequency sweep from start_frequency to end_frequency.

    :param start_frequency: The starting frequency in Hertz (Hz).
    :param end_frequency: The ending frequency in Hertz (Hz).
    :param sound_duration: The duration of the sweep in seconds.
    :param volume: The volume level of the sound (0.0 to 1.0).
    :return: None
    """
    sound = generate_sweep_sound(start_frequency, end_frequency, sound_duration)
    sound.set_volume(volume)
    channel = pygame.mixer.find_channel()  # Get an available channel
    if channel:
        channel.play(sound)


@functools.lru_cache(maxsize=50)
def generate_rumble_sound(frequency, sound_duration, noise_intensity=0.1, noise_frequency=5):
    """
    Generate a low-frequency rumble sound with controllable noise frequency.
    :param frequency: The base frequency of the rumble in Hertz (Hz).
    :param sound_duration: The duration of the sound in seconds.
    :param noise_intensity: How much random noise is added to the sound (0.0 for pure tone, 1.0 for heavy noise).
    :param noise_frequency: The frequency of the noise variations in Hertz (Hz).
    :return: A pygame Sound object of the rumble.
    """
    sample_rate = 44100
    t = np.linspace(0, sound_duration, int(sample_rate * sound_duration), endpoint=False)

    # Base low-frequency wave (a slow sine wave)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Generate low-frequency "noise" using a sine wave combined with randomness
    low_frequency_noise = np.sin(2 * np.pi * noise_frequency * t)
    random_amplitude = np.random.random(size=t.shape) - 0.5  # Random variations
    noise = noise_intensity * low_frequency_noise * random_amplitude

    # Combine the wave and the noise
    rumble = wave + noise

    # Convert to stereo
    stereo_rumble = np.vstack((rumble, rumble)).T

    # Convert the waveform to a format suitable for pygame
    sound = pygame.sndarray.make_sound((32767 * stereo_rumble).astype(np.int16).copy())
    return sound


def play_rumble(frequency, sound_duration, noise_intensity=0.1, volume=0.1):
    """
    Play a low-frequency rumble sound.

    :param frequency: The base frequency of the rumble in Hertz (Hz).
    :param sound_duration: The duration of the rumble in seconds.
    :param noise_intensity: How much random noise to add for a "rumble effect."
    :param volume: The volume level of the rumble sound (0.0 to 1.0).
    :return: None
    """
    sound = generate_rumble_sound(frequency, sound_duration, noise_intensity)
    sound.set_volume(volume)
    sound.play()

@functools.lru_cache(maxsize=50)
def generate_plop_sound(start_frequency, end_frequency, sound_duration=0.2, fade_out_duration=0.15):
    """
    Generate a 'plop' sound effect that starts at a low frequency and sweeps to a higher frequency.

    :param start_frequency: The starting frequency in Hertz (Hz).
    :param end_frequency: The ending frequency in Hertz (Hz).
    :param sound_duration: The total duration of the plop sound, in seconds.
    :param fade_out_duration: The duration over which the sound fades out (less than or equal to sound_duration).
    :return: A pygame Sound object of the plop.
    """
    sample_rate = 44100
    t = np.linspace(0, sound_duration, int(sample_rate * sound_duration), endpoint=False)

    # Generate a logarithmic sweep for rising pitch effect (sounds smooth to the ear)
    frequencies = np.logspace(np.log10(start_frequency), np.log10(end_frequency), len(t))
    wave = 0.5 * np.sin(2 * np.pi * frequencies * t)

    # Apply amplitude envelope (fade out)
    fade = np.ones_like(t)
    fade_out_start = int((sound_duration - fade_out_duration) * sample_rate)
    fade[fade_out_start:] *= np.linspace(1.0, 0.0, len(t) - fade_out_start)
    wave *= fade

    # Convert to stereo
    stereo_wave = np.vstack((wave, wave)).T
    sound = pygame.sndarray.make_sound((32767 * stereo_wave).astype(np.int16).copy())
    return sound


def play_plop(start_frequency=150.0, end_frequency=400.0, sound_duration=0.15, fade_out_duration=0.10, volume=0.2):
    """
    Play a short 'plop' sound effect.

    :param start_frequency: The starting frequency in Hertz (Hz).
    :param end_frequency: The ending frequency in Hertz (Hz).
    :param sound_duration: The duration of the plop sound, in seconds.
    :param fade_out_duration: The duration over which the sound fades out.
    :param volume: The volume level of the plop sound (0.0 to 1.0).
    :return: None
    """
    sound = generate_plop_sound(start_frequency, end_frequency, sound_duration, fade_out_duration)
    sound.set_volume(volume)
    sound.play()

@functools.lru_cache(maxsize=50)
def generate_fanfare_sound(start_frequencies, note_duration=0.2, fade_out_duration=0.1):
    """
    Generate a celebratory "ta-da!" fanfare sound using a sequence of rising notes with harmonies.

    :param start_frequencies: A list or tuple of frequencies (in Hz) for each note in the fanfare.
    :param note_duration: The duration of each note in the fanfare, in seconds.
    :param fade_out_duration: The fade-out at the end of the final note, in seconds.
    :return: A pygame Sound object of the fanfare.
    """
    if isinstance(start_frequencies, list):
        start_frequencies = tuple(start_frequencies)

    # Harmonies to include for each root note frequency (major third, perfect fifth)
    harmony_intervals = [1.25, 1.5]  # Multipliers for the root frequency

    sample_rate = 44100
    total_duration = len(start_frequencies) * note_duration
    t = np.linspace(0, total_duration, int(sample_rate * total_duration), endpoint=False)

    # Initialize an empty waveform
    waveform = np.zeros_like(t)

    # Overlay each note with harmonics into the waveform
    for i, frequency in enumerate(start_frequencies):
        # Time indices for this note
        start_idx = int(i * note_duration * sample_rate)
        end_idx = int((i + 1) * note_duration * sample_rate)
        note_t = t[:end_idx - start_idx]  # Time range for this note

        # Root frequency for the note
        root_wave = 0.5 * np.sin(2 * np.pi * frequency * note_t)

        # Add harmonic frequencies (major third and perfect fifth)
        harmonics_wave = sum(
            0.25 * np.sin(2 * np.pi * (frequency * interval) * note_t) for interval in harmony_intervals
        )

        # Combine the root note with its harmonics
        note_wave = root_wave + harmonics_wave

        # Add the note (with harmonics) to the full waveform
        waveform[start_idx:end_idx] += note_wave

    # Apply fade-out on the final note
    fade_out_start = int((total_duration - fade_out_duration) * sample_rate)
    fade = np.ones_like(t)
    fade[fade_out_start:] = np.linspace(1.0, 0.0, len(t) - fade_out_start)
    waveform *= fade

    # Normalize and convert to stereo
    stereo_waveform = np.vstack((waveform, waveform)).T
    sound = pygame.sndarray.make_sound((32767 * stereo_waveform).astype(np.int16).copy())
    return sound


def play_fanfare(start_frequencies=None, note_duration=0.2, fade_out_duration=0.1, volume=0.3):
    """
    Play a celebratory "ta-da!" fanfare sound.

    :param start_frequencies: A list of frequencies (in Hz) for each note in the fanfare.
    :param note_duration: The duration of each note, in seconds.
    :param fade_out_duration: The fade-out duration at the end of the fanfare.
    :param volume: The volume level for the fanfare.
    :return: None
    """
    if start_frequencies is None:
        start_frequencies = [300.0, 400.0, 600.0]

    if isinstance(start_frequencies, list):
        start_frequencies = tuple(start_frequencies)

    sound = generate_fanfare_sound(start_frequencies, note_duration, fade_out_duration)
    sound.set_volume(volume)
    sound.play()

@functools.lru_cache(maxsize=50)
def generate_lost_game_sound(high_frequency, low_frequency, high_note_duration=0.2, low_note_duration=0.5,
                             fade_out_duration=0.3):
    """
    Generate a sorrowful two-note harmonic sound that signifies loss.

    :param high_frequency: The frequency (in Hz) of the first high note.
    :param low_frequency: The frequency (in Hz) of the second low note.
    :param high_note_duration: The duration of the first high note, in seconds.
    :param low_note_duration: The duration of the second low note, in seconds.
    :param fade_out_duration: The fade-out duration at the end of the low note, in seconds.
    :return: A pygame Sound object of the sorrowful sound.
    """
    # Harmonies for a sorrowful effect (minor third and minor seventh intervals)
    harmony_intervals = [1.2, 0.5]  # Harmonic intervals

    sample_rate = 44100
    total_duration = high_note_duration + low_note_duration
    t = np.linspace(0, total_duration, int(sample_rate * total_duration), endpoint=False)

    # Initialize an empty waveform
    waveform = np.zeros_like(t)

    # Add the high note and its harmonies
    high_start_idx = 0
    high_end_idx = int(high_note_duration * sample_rate)

    high_t = t[high_start_idx:high_end_idx]
    high_root_wave = 0.5 * np.sin(2 * np.pi * high_frequency * high_t)
    high_harmonics_wave = sum(
        0.25 * np.sin(2 * np.pi * (high_frequency * interval) * high_t) for interval in harmony_intervals
    )
    waveform[high_start_idx:high_end_idx] += high_root_wave + high_harmonics_wave

    # Add the low note and its harmonies
    low_start_idx = high_end_idx
    low_end_idx = low_start_idx + int(low_note_duration * sample_rate)

    # Correctly generate `low_t` based on the waveform's slice indices
    low_t = t[low_start_idx:low_end_idx]

    low_root_wave = 0.5 * np.sin(2 * np.pi * low_frequency * low_t)
    low_harmonics_wave = sum(
        0.25 * np.sin(2 * np.pi * (low_frequency * interval) * low_t) for interval in harmony_intervals
    )
    waveform[low_start_idx:low_end_idx] += low_root_wave + low_harmonics_wave

    # Apply fade-out at the end of the low note
    fade_out_start = int((total_duration - fade_out_duration) * sample_rate)
    fade = np.ones_like(t)
    fade[fade_out_start:] = np.linspace(1.0, 0.0, len(t) - fade_out_start)
    waveform *= fade

    # Normalize and convert to stereo
    stereo_waveform = np.vstack((waveform, waveform)).T
    sound = pygame.sndarray.make_sound((32767 * stereo_waveform).astype(np.int16).copy())
    return sound


def play_lost_game_sound(high_frequency=600.0, low_frequency=200.0, high_note_duration=0.2, low_note_duration=0.5,
                         fade_out_duration=0.3, volume=0.3):
    """
    Play a sorrowful two-note harmonic sound that signifies loss.

    :param high_frequency: The frequency (in Hz) of the first high note.
    :param low_frequency: The frequency (in Hz) of the second low note.
    :param high_note_duration: The duration of the first high note, in seconds.
    :param low_note_duration: The duration of the second low note, in seconds.
    :param fade_out_duration: The fade-out duration at the end of the second note.
    :param volume: The volume level for the sound (0.0 to 1.0).
    :return: None
    """
    sound = generate_lost_game_sound(high_frequency, low_frequency, high_note_duration, low_note_duration,
                                     fade_out_duration)
    sound.set_volume(volume)
    sound.play()