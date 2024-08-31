
def create_board(width: int, height: int) -> list[list[dict[str, int]]]:
    return [[{'player_id': 0, 'num_pieces': 0} for _ in range(width)] for _ in range(height)]

class Logic:
    def __init__(self, board: list[list[dict[str, int]]]):
        self.board = board

    def place_piece(self, row: int, col: int, player_id: int):
        board_position = self.board[row][col]
        board_position['player_id'] = player_id
        board_position['num_pieces'] += 1

    def get_position_to_the_left(self, row: int, col: int):
        target_col = col - 1
        if target_col < 0:
            raise ValueError("Target column is less than zero")
        return self.board[row][target_col]

    def get_position_to_the_right(self, row: int, col: int):
        target_col = col + 1
        if target_col >= len(self.board[0]):
            raise ValueError("Target column is greater than or equal to the length of the board")
        return self.board[row][target_col]

    def get_position_above(self, row: int, col: int):
        target_row = row - 1
        if target_row < 0:
            raise ValueError("Target row is less than zero")
        return self.board[target_row][col]

    def get_position_below(self, row: int, col: int):
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
        :return: 
        """

        # Iterate through the index of rows in the board
        row_top: int = 0
        row_bottom: int = len(self.board) - 1
        col_left: int = 0
        col_right: int = len(self.board[0]) - 1

        board_changed: bool = True
        while board_changed:
            board_changed = False
            for row_index in range(len(self.board)):
                for col_index in range(len(self.board[row_index])):
                    print("Before:")
                    self.print_board()
                    if row_index == row_top and col_index == col_left:
                        board_changed = self.process_top_left_corner(col_index, row_index)
                    elif row_index == row_top and col_index == col_right:
                        board_changed = self.process_top_right_corner(col_index, row_index)
                    elif row_index == row_bottom and col_index == col_left:
                        board_changed = self.process_bottom_left_corner(col_index, row_index)
                    elif row_index == row_bottom and col_index == col_right:
                        board_changed = self.process_bottom_right_corner(col_index, row_index)
                    elif row_index == row_top:
                        board_changed = self.process_top_edge(col_index, row_index)
                    elif row_index == row_bottom:
                        board_changed = self.process_bottom_edge(col_index, row_index)
                    elif col_index == col_left:
                        board_changed = self.process_left_edge(col_index, row_index)
                    elif col_index == col_right:
                        board_changed = self.process_right_edge(col_index, row_index)
                    else:
                        board_changed = self.process_inner_position(col_index, row_index)
                    print("After:")
                    self.print_board()
                    if self.winner_determined():
                        return True
        return False

    def print_board(self):
        """
        Prints the board in a formatted grid to the console.
        """
        for row in self.board:
            formatted_row = []
            for cell in row:
                formatted_row.append(f"P{cell['player_id']}:{cell['num_pieces']}")
            print(" | ".join(formatted_row))
        print("\n")

    def winner_determined(self) -> bool:
        """
        Checks to see if every occupied position is owned by one player
        :return: True if there is a winner, False otherwise
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
        if winner:
            print("Winner determined.")
        return winner

    def process_inner_position(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 4:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 4
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_right_edge(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        # move pieces
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 3
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_left_edge(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 3
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_bottom_edge(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 3
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_top_edge(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 3:
            return False
        # change ownership
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 3
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_bottom_right_corner(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        # move pieces
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 2
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_bottom_left_corner(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_above(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.get_position_above(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 2
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_top_right_corner(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_left(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        # move pieces
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_left(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 2
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True

    def process_top_left_corner(self, col_index, row_index):
        if self.board[row_index][col_index]['num_pieces'] < 2:
            return False
        # change ownership
        self.get_position_below(row_index, col_index)['player_id'] = self.board[row_index][col_index]['player_id']
        self.get_position_to_the_right(row_index, col_index)['player_id'] = self.board[row_index][col_index][
            'player_id']
        # move pieces
        self.get_position_below(row_index, col_index)['num_pieces'] += 1
        self.get_position_to_the_right(row_index, col_index)['num_pieces'] += 1
        # deduct pieces from source cell
        self.board[row_index][col_index]['num_pieces'] -= 2
        if self.board[row_index][col_index]['num_pieces'] == 0:
            # unassign cell
            self.board[row_index][col_index]['player_id'] = 0
        return True
