import os
import random
import sys
from copy import deepcopy

import pygame

import computer_logic.basic_strategy
from game_logic import logic
from game_logic.logic import determine_winner
from sound import play_sweep, play_rumble, play_plop, play_fanfare, play_lost_game_sound, play_bonk

COMPUTER_DECISION_DELAY = 300

FRAMERATE = 120

BACKGROUND_COLOR = (180, 180, 180)  # Light grey color
ROWS = 5
COLS = 6
CELL_SIZE = 100
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
PLAYER_COLORS = {1: (255, 0, 0), 2: (0, 255, 0)}
HUMAN_PLAYER_ID = 1
COMPUTER_PLAYER_ID = 2

# todo: save and load game when exiting/starting


# Initialize PyGame
pygame.init()
os.environ['SDL_VIDEODRIVER'] = "x11" # this is needed to run in a Docker container
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.init()
pygame_clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chain Reaction')
font = pygame.font.Font(None, 36)

# Initialize the game logic
board = logic.create_board(ROWS, COLS)
game_logic = logic.Logic(board)
hovered_cell = (-1, -1)
current_player = HUMAN_PLAYER_ID


def throttle():
    """
    Imposes a framerate throttle to regulate the game's frames per second (FPS).

    :return: None
    """
    pygame_clock.tick(FRAMERATE)


def animate_piece_from_cell_to_cell(cell_from_row: int, cell_from_col: int,
                                    cell_to_row: int, cell_to_col: int) -> None:
    """
    Displays the animation of a player piece from one cell to another.
    :param cell_from_row: The row index of the starting cell.
    :param cell_from_col: The column index of the starting cell.
    :param cell_to_row: The row index of the destination cell.
    :param cell_to_col: The column index of the destination cell.
    :return: None
    """
    start_x = cell_from_col * CELL_SIZE + CELL_SIZE // 2
    start_y = cell_from_row * CELL_SIZE + CELL_SIZE // 2
    end_x = cell_to_col * CELL_SIZE + CELL_SIZE // 2
    end_y = cell_to_row * CELL_SIZE + CELL_SIZE // 2

    num_frames = 16

    # Calculate the total animation duration based on frames and framerate
    animation_duration = (num_frames+7) / FRAMERATE

    start_frequency = 650
    end_frequency = 350

    # Use the animation_duration as the sound duration
    sound_duration = animation_duration

    # Play the smooth frequency sweep while animating
    play_sweep(start_frequency, end_frequency, sound_duration)

    for frame in range(num_frames):
        pygame.event.pump()
        interpolate_x = start_x + (end_x - start_x) * frame / num_frames
        interpolate_y = start_y + (end_y - start_y) * frame / num_frames

        refresh_screen()
        pygame.draw.circle(screen, PLAYER_COLORS[current_player],
                           (int(interpolate_x), int(interpolate_y)), CELL_SIZE // 6)
        pygame.draw.circle(screen, (0, 0, 0),
                           (int(interpolate_x), int(interpolate_y)), CELL_SIZE // 6, 1)
        pygame.display.flip()
        throttle()



def draw_grid():
    """
    Draws a grid on the screen based on the number of rows and columns defined.

    :return: None
    """
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def draw_pieces(except_row: int = -1, except_col: int = -1):
    """
    Draws the player pieces for all the cells.
    If except_row and except_col are specified, the pieces are not drawn for that cell.
    This is in support of drawing them separately in the jiggle routine.
    :param except_row: The row index of the cell to be excluded from drawing.
    :param except_col: The column index of the cell to be excluded from drawing.
    :return: None
    """
    for row in range(ROWS):
        for col in range(COLS):
            if row == except_row and col == except_col:
                continue
            num_pieces, player = board[row][col]["num_pieces"], board[row][col]["player_id"]
            if (row, col) == hovered_cell and player == current_player:
                draw_pieces_in_cell(row, col, num_pieces + 1,
                                    PLAYER_COLORS[player], hollow=True)
            elif (row, col) == hovered_cell and player == 0:
                draw_pieces_in_cell(row, col, num_pieces + 1,
                                    PLAYER_COLORS[current_player], hollow=True)
            elif player != 0 and num_pieces > 0:
                draw_pieces_in_cell(row, col, num_pieces, PLAYER_COLORS[player])


def draw_pieces_in_cell(row: int, col: int, num_pieces: int, color: tuple[int, int, int], hollow: bool = False,
                        row_offset_pixels: int = 0, col_offset_pixels: int = 0) -> None:
    """
    Draws the player pieces for the given cell. An optional offset can be specified, in support of the jiggle effect.
    :param row: The row index where the pieces will be drawn.
    :param col: The column index where the pieces will be drawn.
    :param num_pieces: The number of pieces to draw in the cell.
    :param color: The RGB color tuple for the pieces.
    :param hollow: Flag to determine if the circles should be hollow or filled.
    :param row_offset_pixels: Optional pixel offset for the row position.
    :param col_offset_pixels: Optional pixel offset for the column position.
    :return: None
    """
    positions = {
        1: [(0.5, 0.5)],
        2: [(0.3, 0.5), (0.7, 0.5)],
        3: [(0.5, 0.3), (0.3, 0.7), (0.7, 0.7)],
        4: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7)],
        5: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7), (0.5, 0.5)],
    }
    radius = CELL_SIZE // 6  # Radius for the circles

    num_pieces = min(num_pieces, 5)  # Max out at 5 to avoid index error
    draw_positions = positions.get(num_pieces, [])  # Handle the case when num_pieces might be 0

    for pos in draw_positions:
        center_x = col * CELL_SIZE + pos[0] * CELL_SIZE
        center_y = row * CELL_SIZE + pos[1] * CELL_SIZE
        if hollow:
            pygame.draw.circle(screen, color, (int(center_x) + row_offset_pixels,
                                               int(center_y) + col_offset_pixels), radius, 2)
            pygame.draw.circle(screen, (0, 0, 0), (int(center_x) + row_offset_pixels,
                                                   int(center_y) + col_offset_pixels), radius, 1)
        else:
            pygame.draw.circle(screen, color, (int(center_x) + row_offset_pixels,
                                               int(center_y) + col_offset_pixels), radius)
            pygame.draw.circle(screen, (0, 0, 0), (int(center_x) + row_offset_pixels,
                                                   int(center_y) + col_offset_pixels), radius, 1)


def jiggle_cell(row: int, col: int, num_pieces: int, color: tuple[int, int, int], hollow: bool = False) -> None:
    """
    Draws and jiggles the player pieces for the given cell.
    :param row: The row index of the cell to jiggle.
    :param col: The column index of the cell to jiggle.
    :param num_pieces: The number of pieces to draw in the cell.
    :param color: The color of the pieces, represented as an (R, G, B) tuple.
    :param hollow: A boolean flag indicating if the pieces should be hollow.
    :return: None
    """
    animation_duration = .5  # Duration of the animation in seconds
    play_rumble(sound_duration=animation_duration)

    start_time = pygame.time.get_ticks()
    while (pygame.time.get_ticks() - start_time) / 1000 < animation_duration:
        offset_row = random.randint(-2, 2)
        offset_col = random.randint(-2, 2)
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_pieces(
            except_row=row,
            except_col=col)
        draw_pieces_in_cell(row, col, num_pieces, color, hollow,
                            row_offset_pixels=offset_row, col_offset_pixels=offset_col)
        pygame.display.flip()
        throttle()
        pygame.time.delay(50)

    refresh_screen()


def human_turn(current_player_id: int):
    """
    Allows a human to play a turn for the specified player id.
    :param current_player_id: ID of the current player making a move
    :return: None
    """
    global hovered_cell
    global board
    pygame.event.clear()

    mouse_pos = pygame.mouse.get_pos()
    process_mouse_position(mouse_pos)
    refresh_screen()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if hovered_cell != (-1, -1):
                row, col = hovered_cell
                if not game_logic.place_piece(row, col, current_player_id):
                    play_bonk()
                    pass
                else:
                    play_plop(sound_duration=.1)
                    perform_player_animation(current_player_id)
                    refresh_screen()
                    break
        elif event.type == pygame.MOUSEMOTION:
            process_mouse_position(event.pos)
        elif event.type == pygame.WINDOWLEAVE:
            hovered_cell = (-1, -1)
        refresh_screen()


def perform_player_animation(current_player_id: int):
    """
    Performs animation for the played piece for the specified player.
    :param current_player_id: The ID of the player for whom the animation is being performed.
    :return: None
    """
    global hovered_cell, board
    hovered_cell = (-1, -1)
    board = deepcopy(game_logic.board)
    while game_logic.process_board():
        last_row = -1
        last_col = -1
        for board_change in game_logic.board_change_list:
            from_row = board_change["from"]["row"]
            from_col = board_change["from"]["col"]
            if from_row != last_row or from_col != last_col:
                jiggle_cell(from_row, from_col, board[from_row][from_col]["num_pieces"],
                            PLAYER_COLORS[current_player_id])
            last_row = from_row
            last_col = from_col
            to_row = board_change["to"]["row"]
            to_col = board_change["to"]["col"]
            board[from_row][from_col]["num_pieces"] -= 1
            animate_piece_from_cell_to_cell(from_row, from_col,
                                            to_row, to_col)
            board[to_row][to_col]["num_pieces"] += 1
            board[to_row][to_col]["player_id"] = current_player_id
            refresh_screen()
            if determine_winner(board) != 0:
                break
        if determine_winner(board) != 0:
            break
    if determine_winner(board) == 0:
        board = game_logic.board


def process_mouse_position(position: tuple[int, int]):
    """
    Processes the mouse position, in support of drawing the hovered cell preview.
    :param position: A tuple containing the x and y coordinates of the mouse position on the screen.
    :return: None
    """
    global hovered_cell
    mouse_x, mouse_y = position
    if mouse_x == 0 and mouse_y == 0:
        hovered_cell = (-1, -1)
        return
    new_row = mouse_y // CELL_SIZE
    new_col = mouse_x // CELL_SIZE
    if 0 <= new_row < ROWS and 0 <= new_col < COLS:
        hovered_cell = (new_row, new_col)
    else:
        hovered_cell = (-1, -1)


def computer_turn(current_player_id: int, opponent_player_id: int):
    """
    Causes the turn of the specified player to be automatically played by computer logic.
    :param current_player_id: The ID of the current player, representing the computer making a move.
    :param opponent_player_id: The ID of the opponent player.
    :return: None, this function does not return any value.
    """
    global hovered_cell
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
    possible_computer_turns = computer_logic.basic_strategy.find_best_moves(game_logic.board,
                                                                            current_player_id,
                                                                            opponent_player_id)
    best_computer_turn = computer_logic.basic_strategy.choose_one_best_move(possible_computer_turns, 
                                                                           game_logic.board,
                                                                           current_player_id,
                                                                           opponent_player_id)
    wait_for_a_bit(COMPUTER_DECISION_DELAY)
    hovered_cell = best_computer_turn["x"], best_computer_turn["y"]
    refresh_screen()  # redraw with the "hovered" cell where the computer will "click"
    wait_for_a_bit(COMPUTER_DECISION_DELAY)  # give the human a chance to see where the computer is going to "click"
    game_logic.place_piece(best_computer_turn["x"], best_computer_turn["y"], current_player_id)
    play_plop(start_frequency=450, end_frequency=100)
    perform_player_animation(current_player_id)
    hovered_cell = (-1, -1)
    refresh_screen()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def refresh_screen():
    """
    Refreshes the game screen by filling the background, drawing the grid and pieces, and updating the display.
    It also throttles the refresh rate to prevent excessive CPU usage.

    :return: None
    """
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_pieces()
    pygame.display.flip()
    throttle()


def wait_for_a_bit(milliseconds: int):
    """
    Causes a delay in the game without freezing the game or animated mouse cursor.
    :param milliseconds: The amount of time, in milliseconds, to wait.
    :return: None
    """
    end_time = pygame.time.get_ticks() + milliseconds
    while pygame.time.get_ticks() < end_time:
        refresh_screen()


def display_winner(winner: int):
    """
    Shows the winning player number and asks if the player wants to play again.
    :param winner: The player number who has won the game, typically 1 or 2.
    :return: None
    """
    global hovered_cell, current_player, board, game_logic
    hovered_cell = (-1, -1)
    refresh_screen()
    text = font.render(f'{"You win!" if winner == 1 else "Computer wins!"} Play again?', True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect.inflate_ip(6, 6)
    text_rect.move_ip(-3, -3)
    screen.fill((255, 255, 255), text_rect)  # Fill the text area with white
    pygame.draw.rect(screen, (0, 0, 0), text_rect, 2)
    text_rect.move_ip(3, 3)
    screen.blit(text, text_rect)

    # Create Yes/No button
    yes_text = font.render('Yes', True, (0, 0, 0))
    no_text = font.render('No', True, (0, 0, 0))
    yes_rect = yes_text.get_rect(center=(WIDTH // 2 - 50, HEIGHT // 2 + 50))
    no_rect = no_text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 + 50))

    pygame.draw.rect(screen, (255, 255, 255), yes_rect.inflate(20, 20))
    pygame.draw.rect(screen, (0, 0, 0), yes_rect.inflate(20, 20), 2)
    screen.blit(yes_text, yes_rect)

    pygame.draw.rect(screen, (255, 255, 255), no_rect.inflate(20, 20))
    pygame.draw.rect(screen, (0, 0, 0), no_rect.inflate(20, 20), 2)
    screen.blit(no_text, no_rect)

    pygame.display.flip()
    if winner == 1:
        play_fanfare()
    else:
        play_lost_game_sound()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if yes_rect.inflate(20, 20).collidepoint(mouse_pos):
                # Restart the game
                board = logic.create_board(ROWS, COLS)
                game_logic = logic.Logic(board)
                current_player = HUMAN_PLAYER_ID
                hovered_cell = (-1, -1)
                refresh_screen()
                return
            elif no_rect.inflate(20, 20).collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()


def main():
    """
    Handles the main game loop, alternating turns between human and computer players until there's a winner.

    :return: None
    """
    global hovered_cell
    global current_player
    global HUMAN_PLAYER_ID
    global COMPUTER_PLAYER_ID

    while True:
        match current_player:
            case 1:
                human_turn(HUMAN_PLAYER_ID)
            case 2:
                computer_turn(COMPUTER_PLAYER_ID, HUMAN_PLAYER_ID)
        game_over = game_logic.winner_id()
        if game_over:
            display_winner(game_over)
        else:
            current_player = 1 if current_player == 2 else 2  # Toggle player
            hovered_cell = (-1, -1)  # Reset hovered cell after a move


if __name__ == "__main__":
    main()
