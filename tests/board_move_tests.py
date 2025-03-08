import copy
import unittest

from computer_logic.basic_strategy import find_best_moves


class TestFindBestMoves(unittest.TestCase):
    def setUp(self):
        """Sets up initial test conditions."""
        self.board_size = 3
        # Ensure all cells include both 'player_id' and 'num_pieces'
        self.empty_board = [[{"player_id": 0, "num_pieces": 0} for _ in range(self.board_size)] for _ in
                            range(self.board_size)]

    def test_find_best_moves(self):
        """Test to evaluate find_best_moves for all possible setups."""
        player_ids = [1, 2]  # Assuming 1 and 2 are valid player IDs
        for current_player_id in player_ids:
            for opponent_player_id in player_ids:
                if current_player_id == opponent_player_id:
                    continue
                for x in range(self.board_size):
                    for y in range(self.board_size):
                        board = copy.deepcopy(self.empty_board)
                        board[x][y]["player_id"] = opponent_player_id
                        result = find_best_moves(board, current_player_id, opponent_player_id)
                        # Ensure no invalid moves (e.g., scores shouldn't conflict with valid logic)
                        for move in result:
                            with self.subTest(move=move):
                                self.assertIn("x", move)
                                self.assertIn("y", move)
                                self.assertIsInstance(move["score"], int)
                                self.assertGreaterEqual(move["score"], 0)  # Scores should be non-negative