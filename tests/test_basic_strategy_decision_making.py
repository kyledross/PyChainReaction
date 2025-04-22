import unittest

from src.computer_logic import basic_strategy


class TestBasicStrategyDecisionMaking(unittest.TestCase):
    def test_best_move_one_choice(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = basic_strategy.find_best_moves(board, 2, 1)
        best_move = basic_strategy.choose_one_best_move(result, board, 2, 1)
        self.assertEqual(best_move["x"], 0)
        self.assertEqual(best_move["y"], 1)

    def test_best_move_two_choices(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}]
        ]
        result = basic_strategy.find_best_moves(board, 2, 1)
        best_move = basic_strategy.choose_one_best_move(result, board, 2, 1)
        self.assertEqual(best_move["x"], 0)
        self.assertEqual(best_move["y"], 1)

    def test_best_move_two_adjacent_choices(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 2, 'num_pieces': 1}]
        ]
        result = basic_strategy.find_best_moves(board, 2, 1)
        self.assertIn({'x': 2, 'y': 2, 'score': 6}, result)
        best_move = basic_strategy.choose_one_best_move(result, board, 2, 1)
        self.assertIn((best_move["x"], best_move["y"]), [(2, 2)])

    def test_other_players_cells_should_not_be_suggested_moves(self):
        board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 2, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 1}],
            [{'player_id': 2, 'num_pieces': 2}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 1, 'num_pieces': 2}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 1, 'num_pieces': 1}]
        ]
        best_moves = basic_strategy.find_best_moves(board, 2, 1)
        for move in best_moves:
            x, y = move['x'], move['y']
            self.assertNotEqual(board[y][x]['player_id'], 2)

    def test_other_players_cells_should_not_be_suggested_moves_one_spot(self):
        # this came from a real bug.
        # the list of possible best-moves should never include spots that aren't valid, such as the spot taken
        # by an opponent.
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]
        best_moves = basic_strategy.find_best_moves(board, 2, 1)
        for move in best_moves:
            x, y = move['x'], move['y']
            self.assertNotEqual(board[y][x]['player_id'], 1)

    def test_no_possible_moves(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}]
        ]
        with self.assertRaises(ValueError):
            basic_strategy.find_best_moves(board, 2, 1)

if __name__ == '__main__':
    unittest.main()
