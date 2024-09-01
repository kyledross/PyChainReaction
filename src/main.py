from game_logic import logic


def main():
    board = logic.create_board(6, 5)
    game = logic.Logic(board)


if __name__ == "__main__":
    main()
