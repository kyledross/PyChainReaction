import game_logic.logic


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

    
    scored_moves = [{"x": 0, "y": 0, "score": 0}]

    for y in range(board_height):
        for x in range(board_width):
            logic = game_logic.logic.Logic(board.copy())
            if logic.place_piece(y, x, player_id):
                # placement was successful
                # process the board
                board_changed = logic.process_board()
                if not board_changed:
                    scored_moves.append({"x": x, "y": y, "score": 1}) # this move only added a piece
                else:
                    # this move caused a reaction
                    # score the result
                    score: int = 1 # todo: write scoring routine
                    scored_moves.append({"x": x, "y": y, "score": score})
            else:
                scored_moves.append({"x": x, "y": y, "score": 0}) # this move isn't allowed

    #todo: find moves with the highest score
    # if there is more than one with the same rank, randomly choose one

    #todo: return the best x,y move

def score_game_board(board: list[list[dict[str, int]]], player_id: int) -> int:
    #todo: count the number of cells that belong to the player

    return 0