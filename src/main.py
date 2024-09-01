import computer_logic.basic_strategy
from game_logic import logic


def main():
    board = logic.create_board(6, 5)
    game_logic = logic.Logic(board)
    computer1_player_id: int = 1
    computer2_player_id: int = 2

    turn_count: int = 0
    current_player_id: int = computer1_player_id
    winner_id: int = 0
    while winner_id == 0:
        turn_count += 1
        current_player_best_moves = computer_logic.basic_strategy.find_best_moves(
            game_logic.board, current_player_id)
        current_player_best_move = computer_logic.basic_strategy.choose_one_best_move(current_player_best_moves)
        game_logic.place_piece(current_player_best_move["x"], current_player_best_move["y"], current_player_id)
        winner_id = game_logic.process_board()
        print(f"Player {current_player_id} played {current_player_best_move}")
        game_logic.print_board()
        current_player_id = computer2_player_id if current_player_id == computer1_player_id else computer1_player_id

    print(f"Player {winner_id} won in {turn_count} turns.")

if __name__ == "__main__":
    main()
