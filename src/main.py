import computer_logic.basic_strategy
from game_logic import logic


def main():
    board = logic.create_board(3, 3)
    game_logic = logic.Logic(board)
    computer1_player_id = 1
    computer2_player_id = 2

    current_player_id = computer1_player_id
    while not game_logic.winner_determined():
        current_player_best_moves = computer_logic.basic_strategy.find_best_moves(
            game_logic.board, current_player_id)
        current_player_best_move = computer_logic.basic_strategy.choose_one_best_move(current_player_best_moves)
        game_logic.place_piece(current_player_best_move["x"], current_player_best_move["y"], current_player_id)
        game_logic.process_board()
        print(f"Player {current_player_id} played {current_player_best_move}")
        game_logic.print_board()
        current_player_id = computer2_player_id if current_player_id == computer1_player_id else computer1_player_id


if __name__ == "__main__":
    main()
