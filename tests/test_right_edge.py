import unittest

from logic.logic import Logic


class TestLogic(unittest.TestCase):

    def setUp(self):
        self.logic = Logic()

    def test_process_right_edge(self):
        self.logic.board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 3}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = self.logic.process_right_edge(2, 1)
        self.assertEqual(result, True)
        self.assertEqual(self.logic.board, [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}]
        ])

        self.logic.board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 2}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]
        result = self.logic.process_right_edge(2,1)
        self.assertEqual(result, False)
        self.assertEqual(self.logic.board, [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 2}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ])


if __name__ == "__main__":
    unittest.main()
