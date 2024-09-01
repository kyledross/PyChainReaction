import unittest

from game_logic import logic
from game_logic.logic import Logic


class TestLogic(unittest.TestCase):

    def setUp(self):
        self.logic = Logic(logic.create_board(1, 1))


    def test_winner_determination(self):
        self.logic.board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 1, 'num_pieces': 1}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = self.logic.winner_determined()
        self.assertEqual(result, True)

        self.logic.board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 1}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = self.logic.winner_determined()
        self.assertEqual(result, False)

        self.logic.board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = self.logic.winner_determined()
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
