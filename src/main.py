import pygame
import sys

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Board')
font = pygame.font.Font(None, 36)

# Initialize the game logic
board = logic.create_board(ROWS, COLS)
game_logic = logic.Logic(board)
hovered_cell = (-1, -1)
current_player = 1


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hovered_cell != (-1, -1):
                    row, col = hovered_cell
                    if not game_logic.place_piece(row, col, current_player):
                        print("Invalid move, try again.")
                    else:
                        game_over = game_logic.process_board()
                        if game_over:
                            display_winner(game_over)
                        current_player = 1 if current_player == 2 else 2  # Toggle player
                        hovered_cell = (-1, -1)  # Reset hovered cell after a move

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                new_row = mouse_y // CELL_SIZE
                new_col = mouse_x // CELL_SIZE

                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    hovered_cell = (new_row, new_col)
                else:
                    hovered_cell = (-1, -1)

        refresh_screen()


def refresh_screen():
    screen.fill((255, 255, 255))
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