import game_logic.logic
import random
import copy


def find_best_play(board: list[list[dict[str, int]]], player_id: int):
    """
    This routine will iteratively attempt to place a piece on each cell of a board, and then
    process the board for each move to see how effective the move was.  It scores each attempted move,
    and then returns the best x,y move based on the highest score.
    :param board: the game board
    :param player_id: the id of the player making the move
    :return: x,y of the best move
    """
    board_width = len(board[0])
    board_height = len(board)

    
    scored_moves = []

    for y in range(board_height):
        for x in range(board_width):
            logic = game_logic.logic.Logic(copy.deepcopy(board))
            if logic.place_piece(y, x, player_id):
                # placement was successful
                # process the board
                board_changed = logic.process_board()
                # this move caused a reaction
                # score the result
                score: int = score_game_board(logic.board, player_id)
                scored_moves.append({"x": x, "y": y, "score": score})
            else:
                scored_moves.append({"x": x, "y": y, "score": 0}) # this move isn't allowed


    # Find the highest score
    highest_score = max(move["score"] for move in scored_moves)

    # Collect all moves with the highest score
    best_moves = [move for move in scored_moves if move["score"] == highest_score]

    # Randomly select one of the best moves if there are ties
    best_move = random.choice(best_moves)

    # Return the coordinates of the best move
    return best_move["x"], best_move["y"]

def score_game_board(board: list[list[dict[str, int]]], player_id: int) -> int:
    count = 0
    for row in board:
        for cell in row:
            if cell.get("player_id") == player_id:
                count += 1
    return count