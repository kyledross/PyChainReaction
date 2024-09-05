import pygame
import sys

import computer_logic.basic_strategy
from game_logic import logic

# Constants
ROWS = 5
COLS = 6
CELL_COLOR = (255, 255, 255)
HOVER_COLOR = (0, 0, 0)
CELL_SIZE = 100
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
PLAYER_COLORS = {1: (0, 255, 0), 2: (255, 0, 0)}

# Initialize PyGame
pygame.init()
pygame_clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chain Reaction')
font = pygame.font.Font(None, 36)

# Initialize the game logic
board = logic.create_board(ROWS, COLS)
game_logic = logic.Logic(board)
hovered_cell = (-1, -1)
current_player = 1


def throttle():
    pygame_clock.tick(120)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            num_pieces, player = board[row][col]["num_pieces"], board[row][col]["player_id"]
            if (row, col) == hovered_cell and player == current_player:
                draw_piece(row, col, num_pieces + 1, PLAYER_COLORS[player], hollow=True)
            elif (row, col) == hovered_cell and player == 0:
                draw_piece(row, col, num_pieces + 1, PLAYER_COLORS[current_player], hollow=True)
            elif player != 0:
                draw_piece(row, col, num_pieces, PLAYER_COLORS[player])


def draw_piece(row, col, num_pieces, color, hollow=False):
    positions = {
        1: [(0.5, 0.5)],
        2: [(0.3, 0.5), (0.7, 0.5)],
        3: [(0.5, 0.3), (0.3, 0.7), (0.7, 0.7)],
        4: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7)]
    }
    radius = CELL_SIZE // 6  # Radius for the circles

    num_pieces = min(num_pieces, 4)  # Max out at 4 to avoid index error
    draw_positions = positions[num_pieces]

    for pos in draw_positions:
        center_x = col * CELL_SIZE + pos[0] * CELL_SIZE
        center_y = row * CELL_SIZE + pos[1] * CELL_SIZE
        if hollow:
            pygame.draw.circle(screen, color, (int(center_x), int(center_y)), radius, 2)
        else:
            pygame.draw.circle(screen, color, (int(center_x), int(center_y)), radius)


def main():
    global hovered_cell
    global current_player
    opponent_player = 1
    while True:
        match current_player:
            case 1:
                human_turn(current_player)
            case 2:
                computer_turn(current_player, opponent_player)
        game_over = game_logic.winner_id()
        if game_over:
            display_winner(game_over)
            break
        current_player = 1 if current_player == 2 else 2  # Toggle player
        hovered_cell = (-1, -1)  # Reset hovered cell after a move


def human_turn(current_player_id):
    global hovered_cell
    pygame.event.clear()

    mouse_pos = pygame.mouse.get_pos()
    process_mouse_position(mouse_pos)
    refresh_screen()
    while True:
        throttle()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if hovered_cell != (-1, -1):
                row, col = hovered_cell
                if not game_logic.place_piece(row, col, current_player_id):
                    # todo: add invalid move sound feedback here
                    pass
                else:

                    while game_logic.process_board():
                        # todo: implement animation here
                        pass
                    hovered_cell = (-1, -1)
                    refresh_screen()
                    break
        elif event.type == pygame.MOUSEMOTION:
            process_mouse_position(event.pos)
        elif event.type == pygame.WINDOWLEAVE:
            hovered_cell = (-1, -1)
        refresh_screen()


def process_mouse_position(position):
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
    global hovered_cell
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
    possible_computer_turns = computer_logic.basic_strategy.find_best_moves(game_logic.board, current_player_id,
                                                                            opponent_player_id)
    best_computer_turn = computer_logic.basic_strategy.choose_one_best_move(possible_computer_turns)
    pygame.time.wait(500)
    hovered_cell = best_computer_turn["x"], best_computer_turn["y"]
    refresh_screen()
    pygame.time.wait(500)
    game_logic.place_piece(best_computer_turn["x"], best_computer_turn["y"], current_player_id)
    while game_logic.process_board():
        # todo: implement animation here
        pass
    hovered_cell = (-1, -1)
    refresh_screen()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def refresh_screen():
    screen.fill((169, 169, 169))
    draw_grid()
    draw_pieces()
    pygame.display.flip()


def display_winner(winner):
    global hovered_cell
    hovered_cell = (-1, -1)
    refresh_screen()
    text = font.render(f'Player {winner} wins!', True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rect.inflate_ip(6, 6)
    text_rect.move_ip(-3, -3)
    screen.fill((255, 255, 255), text_rect)  # Fill the text area with white
    pygame.draw.rect(screen, (0, 0, 0), text_rect, 2)  # Draw a black border around the text area
    text_rect.move_ip(3, 3)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
