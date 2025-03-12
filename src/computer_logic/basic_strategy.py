import random
import copy

from game_logic.logic import Logic

# todo: create strategy for looking for opponent cells that are full and look at surrounding cells for current_player cells that are also full and rank those cells much higher

def find_best_moves(board: list[list[dict[str, int]]], current_player_id: int, opponent_player_id: int) -> list[dict[str, int]]:
    """
    This routine will iteratively attempt to place a piece on each cell of a board, and then
    process the board for each move to see how effective the move was.  It scores each attempted move,
    and then returns a list of the best moves.
    :param board: the game board
    :param current_player_id: the id of the player making the move
    :param opponent_player_id: the id of the opponent player
    :return: List of x,y, and score of the best moves
    """
    board_width = len(board[0])
    board_height = len(board)

    scored_moves = []

    for x in range(board_height):
        for y in range(board_width):
            logic_instance = Logic(copy.deepcopy(board))
            current_player_score_before_placing = score_game_board(board, current_player_id)
            if logic_instance.place_piece(x, y, current_player_id):
                while logic_instance.process_board():
                    if logic_instance.winner_id() != 0:
                        break
                current_player_score_after_placing: int = score_game_board(logic_instance.board, current_player_id)
                opponent_before_score: int = score_game_board(board, opponent_player_id)
                opponent_after_score: int = score_game_board(logic_instance.board, opponent_player_id)
                if current_player_score_after_placing - current_player_score_before_placing == 1:
                    # this move did nothing more than add a piece
                    # 1 point penalty in scoring
                    current_player_score_after_placing -= 1
                current_player_score_after_placing += opponent_before_score - opponent_after_score
                scored_moves.append({"x": x, "y": y, "score": current_player_score_after_placing})

    # Find the highest score
    highest_score = max(move["score"] for move in scored_moves)

    # Collect all moves with the highest score
    best_moves = [move for move in scored_moves if move["score"] == highest_score]

    return best_moves


def choose_one_best_move(best_moves: list[dict[str, int]]) -> dict[str, int]:
    """
    Returns a single best move x, y from a list of 1 or more "best" moves.
    If there are more than one best move, one will be chosen at random.
    :param best_moves: A list of dictionaries containing possible best moves with their coordinates.
    :return: A dictionary containing the x and y coordinates of the chosen best move.
    """
    best_move = random.choice(best_moves)
    return {"x": best_move["x"], "y": best_move["y"]}


def score_game_board(board: list[list[dict[str, int]]], player_id: int) -> int:
    """
    Scores a game board by counting the number of cells associated with a specific player.
    :param board: A 2D list of dictionaries where each dictionary contains game-related attributes like 'player_id'.
    :param player_id: An integer representing the player whose score is to be calculated.
    :return: An integer representing the score of the specific player by counting the cells associated with the
    player_id in the game board.
    """
    count = 0
    for row in board:
        for cell in row:
            if cell.get("player_id") == player_id:
                count += 1
    return count

