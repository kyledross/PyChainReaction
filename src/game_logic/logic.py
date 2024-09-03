def create_board(height: int, width: int) -> list[list[dict[str, int]]]:
    return [[{'player_id': 0, 'num_pieces': 0} for _ in range(width)] for _ in range(height)]


def validate_player_id(player_id: int):
    if player_id != 1 and player_id != 2:
        raise ValueError(f"Player id {player_id} is not valid.")


class Logic:
    """
    Logic class handles the state and operations on a game board consisting of pieces placed by players.

    :param board: A 2D list representing the game board. Each cell is a dictionary containing 'player_id' and 'num_pieces'.
    """

    def __init__(self, board: list[list[dict[str, int]]]):
        self.board = board
        self.send_debug_to_console: bool = False
        self.board_change_list = []

    def validate_board_boundaries(self, row: int, col: int):
        """
        :param row: The row index where the piece is attempted to be placed.
        :param col: The column index where the piece is attempted to be placed.
        :return: None. Raises a ValueError if the row or column is outside the board boundaries.
        """
        if row < 0:
            raise ValueError("Row can't be less than 0.")
        if row >= len(self.board):
            raise ValueError(f"A piece can't be placed at row {row} because the board only has {len(self.board)} rows.")
        if col < 0:
            raise ValueError("Column can't be less than 0.")
        if col < 0 or col >= len(self.board[0]):
            raise ValueError(
                f"A piece can't be placed at column {col} because the board only has {len(self.board[0])} columns.")

    def piece_placement_is_allowed(self, row: int, col: int, player_id: int) -> bool:
        """
        Checks to see if the specified player can place a piece at the specified location.
        This is driven by whether or not another player's piece is already at the location.
        :param row: The row index on the board where the player wants to place the piece.
        :param col: The column index on the board where the player wants to place the piece.
        :param player_id: The identifier for the player attempting to place the piece.
        :return: A boolean value indicating whether the piece placement is allowed based on the game rules and current board state.
        """
        self.validate_board_boundaries(row, col)
        validate_player_id(player_id)
        board_position = self.board[row][col]
        if board_position['player_id'] == 0:
            return True
        if board_position['player_id'] == player_id:
            return True
        return False

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """
        Places a piece belonging to the specified player on the board.
        If the cell already belongs to another player, the placement fails and False is returned.
        :param row: the row to place the piece
        :param col: the column to place the piece
        :param player_id: the id of the player whose pieces are being placed
        :return: True if the placement is successful, False otherwise
        """
        self.validate_board_boundaries(row, col)
        validate_player_id(player_id)
        if not self.piece_placement_is_allowed(row, col, player_id):
            return False
        board_position = self.board[row][col]
        board_position['player_id'] = player_id
        board_position['num_pieces'] += 1
        return True

    def add_move_to_board_change_list(self, row: int, col: int, target_row: int, target_col: int):
        """
        :param row: The row index of the current position on the board.
        :param col: The column index of the current position on the board.
        :param target_row: The row index of the target position to move to.
        :param target_col: The column index of the target position to move to.
        :return: None
        """

        move = {
            'from': {'row': row, 'col': col},
            'to': {'row': target_row, 'col': target_col}
        }
        self.board_change_list.append(move)

    def get_position_to_the_left(self, row: int, col: int) -> dict:
        """
        :param row: The row index of the current position.
        :param col: The column index of the current position.
        :return: The value of the position to the immediate left of the given position.
        :raises ValueError: If there is no position to the left.
        """
        self.validate_board_boundaries(row, col)
        target_col = col - 1
        if target_col < 0:
            raise ValueError("Target column is less than zero")
        return self.board[row][target_col]

    def get_position_to_the_right(self, row: int, col: int) -> dict:
        """
        :param row: The row index of the current position.
        :param col: The column index of the current position.
        :return: The value at the position to the right of the current position as a dictionary.
        :raises ValueError: If there is no position to the right.
        """
        self.validate_board_boundaries(row, col)
        target_col = col + 1
        if target_col >= len(self.board[0]):
            raise ValueError("Target column is greater than or equal to the length of the board")
        return self.board[row][target_col]

    def get_position_above(self, row: int, col: int) -> dict:
        """
        :param row: The current row index of the position
        :param col: The current column index of the position
        :return: The element at the position directly above the given row and column in the board
        :raises ValueError: If there is no position above the given position.
        """
        self.validate_board_boundaries(row, col)
        target_row = row - 1
        if target_row < 0:
            raise ValueError("Target row is less than zero")
        return self.board[target_row][col]

    def get_position_below(self, row: int, col: int) -> dict:
        """
        :param row: The row index of the current position.
        :param col: The column index of the current position.
        :return: The element in the position directly below the specified (row, col) on the board if it exists.
        :raises ValueError: If there is no position below the given position.
        """
        self.validate_board_boundaries(row, col)
        target_row = row + 1
        if target_row >= len(self.board):
            raise ValueError("Target row is greater than or equal to the length of the board")
        return self.board[target_row][col]

    def process_board(self) -> bool:
        """
        Process board will go through each row and column and check to see if there are too many pieces in the position.
        The corner positions can have up to 2 pieces max.
        The side and top positions can have up to 3 pieces max.
        All other positions can have up to 4 pieces max.
        When a position exceeds these limits, one piece is "moved" from that position into each of the positions
        above, below, and to the sides (taking into consideration that corner pieces have two positions they can move
        to, and side positions have three).
        This process continues iteratively until no more cells exceed their limits or all positions on the board contain
        one player's pieces.
        :return: True if another round of processing might be needed, False otherwise.
        """

        # Iterate through the index of rows in the board
        row_top: int = 0
        row_bottom: int = len(self.board) - 1
        col_left: int = 0
        col_right: int = len(self.board[0]) - 1
        self.board_change_list = []
        board_changed = False
        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                if self.send_debug_to_console:
                    print("Before:")
                    self.print_board()
                if row_index == row_top and col_index == col_left:
                    board_changed = self.process_top_left_corner(col_index, row_index) or board_changed
                elif row_index == row_top and col_index == col_right:
                    board_changed = self.process_top_right_corner(col_index, row_index) or board_changed
                elif row_index == row_bottom and col_index == col_left:
                    board_changed = self.process_bottom_left_corner(col_index, row_index) or board_changed
                elif row_index == row_bottom and col_index == col_right:
                    board_changed = self.process_bottom_right_corner(col_index, row_index) or board_changed
                elif row_index == row_top:
                    board_changed = self.process_top_edge(col_index, row_index) or board_changed
                elif row_index == row_bottom:
                    board_changed = self.process_bottom_edge(col_index, row_index) or board_changed
                elif col_index == col_left:
                    board_changed = self.process_left_edge(col_index, row_index) or board_changed
                elif col_index == col_right:
                    board_changed = self.process_right_edge(col_index, row_index) or board_changed
                else:
                    board_changed = self.process_inner_position(col_index, row_index) or board_changed
                if self.send_debug_to_console:
                    print("After:")
                    self.print_board()
        # if there is a winner, no more processing is needed
        if self.winner_id() != 0:
            return False
        return board_changed

    def print_board(self) -> None:
        """
        Prints the board in a formatted grid to the console.
        """
        print("x")
        for row_index, row in enumerate(self.board):
            formatted_row = [f"{row_index} "]  # Add row number
            for cell in row:
                formatted_row.append(f"P{cell['player_id']}:{cell['num_pieces']}")
            print(" | ".join(formatted_row))

        # Print column headers
        col_headers = "y  | " + " | ".join(f"{col_index}   " for col_index in range(len(self.board[0])))
        print(col_headers)
        print()

    def winner_id(self) -> int:
        """
        Checks to see if every occupied position is owned by one player
        :return: Winning player id, 0 if there is no winner.
        """
        occupied_count: int = 0
        player_1_count: int = 0
        player_2_count: int = 0

        for row in self.board:
            for cell in row:
                if cell['player_id'] != 0:
                    occupied_count += 1
                    if cell['player_id'] == 1:
                        player_1_count += 1
                    if cell['player_id'] == 2:
                        player_2_count += 1
        winner = occupied_count > 1 and (occupied_count == player_1_count or occupied_count == player_2_count)
        if winner and self.send_debug_to_console:
            print("Winner determined.")
        if winner and player_1_count != 0:
            return 1
        elif winner and player_2_count != 0:
            return 2
        else:
            return 0

    def process_inner_position(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is not a corner or edge.
        :param col_index: The column index of the position to be processed.
        :param row_index: The row index of the position to be processed.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 4:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.move_piece_up(row_index, col_index)
        self.move_piece_down(row_index, col_index)
        self.move_piece_left(row_index, col_index)
        self.move_piece_right(row_index, col_index)
        return True

    def move_piece_right(self, row_index, col_index):
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        self.board[row_index][col_index]['num_pieces'] -= 1
        self.unassign_empty_cell(col_index, row_index)
        self.add_move_to_board_change_list(row_index, col_index, row_index, col_index + 1)

    def move_piece_left(self, row_index, col_index):
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        self.board[row_index][col_index]['num_pieces'] -= 1
        self.unassign_empty_cell(col_index, row_index)
        self.add_move_to_board_change_list(row_index, col_index, row_index, col_index - 1)

    def move_piece_up(self, row_index, col_index):
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.board[row_index][col_index]['num_pieces'] -= 1
        self.unassign_empty_cell(col_index, row_index)
        self.add_move_to_board_change_list(row_index, col_index, row_index - 1, col_index)

    def move_piece_down(self, row_index, col_index):
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.board[row_index][col_index]['num_pieces'] -= 1
        self.unassign_empty_cell(col_index, row_index)
        self.add_move_to_board_change_list(row_index, col_index, row_index + 1, col_index)

    def unassign_empty_cell(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0

    def process_right_edge(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a right edge, but not a corner.
        :param col_index: The column index of the position on the board to be processed.
        :param row_index: The row index of the position on the board to be processed.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        # move pieces
        self.move_piece_up(row_index, col_index)
        self.move_piece_down(row_index, col_index)
        self.move_piece_left(row_index, col_index)
        return True

    def process_left_edge(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a left edge, but not a corner.
        :param col_index: The column index of the cell being processed.
        :param row_index: The row index of the cell being processed.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.move_piece_up(row_index, col_index)
        self.move_piece_down(row_index, col_index)
        self.move_piece_right(row_index, col_index)
        return True

    def process_bottom_edge(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a bottom edge, but not a corner.
        :param col_index: The column index of the cell being processed on the board.
        :param row_index: The row index of the cell being processed on the board.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.move_piece_up(row_index, col_index)
        self.move_piece_left(row_index, col_index)
        self.move_piece_right(row_index, col_index)
        return True

    def process_top_edge(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a top edge, but not a corner.
        :param col_index: Column index of the cell being processed
        :param row_index: Row index of the cell being processed
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.move_piece_down(row_index, col_index)
        self.move_piece_left(row_index, col_index)
        self.move_piece_right(row_index, col_index)
        return True

    def process_bottom_right_corner(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a bottom right corner.
        :param col_index: The column index of the cell being processed.
        :param row_index: The row index of the cell being processed.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        # move pieces
        self.move_piece_up(row_index, col_index)
        self.move_piece_left(row_index, col_index)
        return True

    def process_bottom_left_corner(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a bottom left corner.
        :param col_index: The index of the column where the cell is located.
        :param row_index: The index of the row where the cell is located.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.move_piece_up(row_index, col_index)
        self.move_piece_right(row_index, col_index)
        return True

    def process_top_right_corner(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a top right corner.
        :param col_index: The column index of the cell being processed.
        :param row_index: The row index of the cell being processed.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        # move pieces
        self.move_piece_down(row_index, col_index)
        self.move_piece_left(row_index, col_index)
        return True

    def process_top_left_corner(self, col_index: int, row_index: int) -> bool:
        """
        Processes a cell that is a top left corner.
        :param col_index: The column index of the board position.
        :param row_index: The row index of the board position.
        :return: A boolean value indicating whether the processing resulted in a chain reaction.
        """
        self.validate_board_boundaries(row_index, col_index)
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.move_piece_down(row_index, col_index)
        self.move_piece_right(row_index, col_index)
        return True
