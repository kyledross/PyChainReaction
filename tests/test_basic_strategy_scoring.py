import unittest

from src.computer_logic import basic_strategy


class TestBasicStrategy(unittest.TestCase):
    def setUp(self):
        self.player_id = 1
        self.board = [
            [{'player_id': 1}, {'player_id': 1}, {'player_id': 2}],
            [{'player_id': 2}, {'player_id': 2}, {'player_id': 1}],
            [{'player_id': 1}, {'player_id': 1}, {'player_id': 1}]
        ]

    def test_score_game_board_with_valid_input(self):
        expected_score = 6
        actual_score = basic_strategy.score_game_board(self.board, self.player_id)
        self.assertEqual(expected_score, actual_score)

    def test_score_game_board_with_no_player_cells(self):
        no_player_board = [
            [{'player_id': 2}, {'player_id': 2}, {'player_id': 2}],
            [{'player_id': 2}, {'player_id': 2}, {'player_id': 2}],
            [{'player_id': 2}, {'player_id': 2}, {'player_id': 2}]
        ]
        expected_score = 0
        actual_score = basic_strategy.score_game_board(no_player_board, self.player_id)
        self.assertEqual(expected_score, actual_score)

    def test_score_game_board_with_all_player_cells(self):
        all_player_board = [
            [{'player_id': 1}, {'player_id': 1}, {'player_id': 1}],
            [{'player_id': 1}, {'player_id': 1}, {'player_id': 1}],
            [{'player_id': 1}, {'player_id': 1}, {'player_id': 1}]
        ]
        expected_score = 9
        actual_score = basic_strategy.score_game_board(all_player_board, self.player_id)
        self.assertEqual(expected_score, actual_score)


if __name__ == '__main__':
    unittest.main()
