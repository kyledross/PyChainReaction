import unittest

from src.computer_logic import basic_strategy


class TestBasicStrategyDecisionMaking(unittest.TestCase):
    def test_best_move_one_choice(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = basic_strategy.find_best_play(board, 2)
        best_move = basic_strategy.choose_one_best_move(result)
        self.assertEqual(
            best_move,
            (1, 0))

    def test_best_move_two_choices(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}]
        ]
        result = basic_strategy.find_best_play(board, 2)
        best_move = basic_strategy.choose_one_best_move(result)
        self.assertEqual(
            best_move,
            (1, 0))

    def test_best_move_two_choices_yield_same_result(self):
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 2, 'num_pieces': 1}]
        ]
        result = basic_strategy.find_best_play(board, 2)
        self.assertIn({'x': 1, 'y': 2, 'score': 4}, result)
        self.assertIn({'x': 2, 'y': 2, 'score': 4}, result)
        best_move = basic_strategy.choose_one_best_move(result)
        self.assertIn(best_move, [(1, 2), (2, 2)])


if __name__ == '__main__':
    unittest.main()