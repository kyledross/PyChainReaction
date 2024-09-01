from game_logic import logic
from game_logic.logic import Logic


def main():
    board = logic.create_board(6, 5)
    game = Logic(board)


if __name__ == "__main__":
    main()
