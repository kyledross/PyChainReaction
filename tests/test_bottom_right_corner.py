import unittest

from logic.logic import Logic


class TestLogic(unittest.TestCase):

    def setUp(self):
        self.logic = Logic()

    def test_process_bottom_right_corner(self):
        self.logic.board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 2}]
        ]
        result = self.logic.process_bottom_right_corner(1, 1)
        self.assertEqual(result, True)
        self.assertEqual(self.logic.board, [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}]
        ])

        self.logic.board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}]
        ]
        result = self.logic.process_bottom_right_corner(0,1)
        self.assertEqual(result, False)
        self.assertEqual(self.logic.board, [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}]
        ])


if __name__ == "__main__":
    unittest.main()
