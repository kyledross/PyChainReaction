import functools
import numpy as np
import pygame


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
    t = np.linspace(0, sound_duration, int(sample_rate * sound_duration), endpoint=False)

    # Use a smooth interpolation for frequency (logarithmic chirp is smoother than linear)
    frequencies = np.logspace(np.log10(start_frequency), np.log10(end_frequency), num=len(t))

    # Create the waveform for the frequency sweep
    wave = 0.5 * np.sin(2 * np.pi * frequencies * t)

    # Convert the waveform to stereo
    stereo_wave = np.vstack((wave, wave)).T

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
    pygame.mixer.stop()  # Stop any currently playing sounds
    sound.set_volume(volume)
    sound.play()
    pygame.mixer.stop()  # Stop any currently playing sounds
    sound.set_volume(volume)
    sound.play()


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
