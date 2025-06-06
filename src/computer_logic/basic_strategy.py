import random
import copy
from typing import Any

from game_logic.logic import Logic

# Number of iterations to look ahead when evaluating moves
LOOK_AHEAD_ITERATIONS = 3

# todo: create strategy for looking for opponent cells that are full and look at surrounding cells for current_player cells that are also full and rank those cells much higher

def find_best_moves(board: list[list[dict[str, int]]], current_player_id: int, opponent_player_id: int) -> list[dict[str, int]]:
    """
    This routine will iteratively attempt to place a piece on each cell of a board and then
    process the board for each move to see how effective the move was.
    It scores each attempted move
    and then returns a list of the best moves.
    :param board: The game board
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
                    # 1-point penalty in scoring
                    current_player_score_after_placing -= 1
                current_player_score_after_placing += opponent_before_score - opponent_after_score
                scored_moves.append({"x": x, "y": y, "score": current_player_score_after_placing})

    if not scored_moves:
        raise ValueError("There were no moves possible. This should never happen.")

    # Find the highest score
    highest_score = max(move["score"] for move in scored_moves)

    # Collect all moves with the highest score
    best_moves = [move for move in scored_moves if move["score"] == highest_score]

    return best_moves


def evaluate_move_with_look_ahead(move: dict[str, int], board: list[list[dict[str, int]]], 
                              current_player_id: int, opponent_player_id: int, 
                              depth: int = LOOK_AHEAD_ITERATIONS) -> float | int | Any:
    """
    Evaluates a move by simulating future moves up to the specified depth.

    :param move: The move to evaluate (x, y coordinates)
    :param board: The current game board
    :param current_player_id: ID of the current player
    :param opponent_player_id: ID of the opponent player
    :param depth: How many moves ahead to look
    :return: A score representing how good the move is after looking ahead
    """
    # Base case: if we've reached the maximum depth or the game is over
    if depth <= 0:
        return score_game_board(board, current_player_id) - score_game_board(board, opponent_player_id)

    # Create a copy of the board to simulate the move
    logic_instance = Logic(copy.deepcopy(board))

    # Try to place the piece
    if not logic_instance.place_piece(move["x"], move["y"], current_player_id):
        # If the move is invalid, return a very low score
        return float('-inf')

    # Process the board after placing the piece
    while logic_instance.process_board():
        if logic_instance.winner_id() != 0:
            # If this move leads to a win, return a very high score
            if logic_instance.winner_id() == current_player_id:
                return float('inf')
            # If this move leads to a loss, return a very low score
            else:
                return float('-inf')

    # If this is the last depth level, just return the score
    if depth == 1:
        return score_game_board(logic_instance.board, current_player_id) - score_game_board(logic_instance.board, opponent_player_id)

    # Find the best moves for the opponent
    opponent_best_moves = find_best_moves(logic_instance.board, opponent_player_id, current_player_id)

    # If there are no valid moves for the opponent, this is good for us
    if not opponent_best_moves:
        return float('inf')

    # Evaluate each of the opponent's best moves and take the minimum score
    # (since the opponent will choose the move that's worst for us)
    min_score = float('inf')
    for opponent_move in opponent_best_moves:
        # Recursively evaluate the opponent's move, but from their perspective
        opponent_score = evaluate_move_with_look_ahead(
            opponent_move, 
            logic_instance.board, 
            opponent_player_id, 
            current_player_id, 
            depth - 1
        )
        # The opponent's score is the negative of our score
        our_score = -opponent_score
        min_score = min(min_score, our_score)

    return min_score


def choose_one_best_move(best_moves: list[dict[str, int]], board: list[list[dict[str, int]]], 
                         current_player_id: int, opponent_player_id: int) -> dict[str, int]:
    """
    Returns the single best move x, y from a list of 1 or more "best" moves.
    Evaluates each move by looking ahead multiple iterations and chooses the one
    with the best outcome.

    :param best_moves: A list of dictionaries containing possible best moves with their coordinates.
    :param board: The current game board
    :param current_player_id: ID of the current player
    :param opponent_player_id: ID of the opponent player
    :return: A dictionary containing the x and y coordinates of the chosen best move.
    """
    # If there's only one best move, return it
    if len(best_moves) == 1:
        return {"x": best_moves[0]["x"], "y": best_moves[0]["y"]}

    # Evaluate each move with look-ahead
    move_scores = []
    for move in best_moves:
        score = evaluate_move_with_look_ahead(move, board, current_player_id, opponent_player_id)
        move_scores.append({"x": move["x"], "y": move["y"], "score": score})

    # Find the highest score after look-ahead
    highest_score = max(move["score"] for move in move_scores)

    # Collect all moves with the highest score
    best_moves_after_look_ahead = [move for move in move_scores if move["score"] == highest_score]

    # If there are multiple moves with the same score, choose one randomly
    best_move = random.choice(best_moves_after_look_ahead)
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
