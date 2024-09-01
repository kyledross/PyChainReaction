import unittest

from src.game_logic.logic import Logic


class TestLogicMethods(unittest.TestCase):

    def setUp(self):
        self.logic = Logic([[
            {'player_id': 0, 'num_pieces': 0},
            {'player_id': 1, 'num_pieces': 1},
            {'player_id': 2, 'num_pieces': 1}],

            [{'player_id': 0, 'num_pieces': 1},
             {'player_id': 1, 'num_pieces': 1},
             {'player_id': 2, 'num_pieces': 1}],

            [{'player_id': 0, 'num_pieces': 2},
             {'player_id': 1, 'num_pieces': 2},
             {'player_id': 2, 'num_pieces': 2}]
        ])

    def test_validate_board_boundaries_correct_ranges(self):
        # Test that the method does not raise an error for an in-bound row and column
        try:
            self.logic.validate_board_boundaries(0, 0)
            self.logic.validate_board_boundaries(1, 1)
            self.logic.validate_board_boundaries(2, 2)
        except ValueError:
            self.fail("validate_board_boundaries() raised ValueError unexpectedly!")

    def test_validate_board_boundaries_negative_ranges(self):
        # Test that the method raises an error for negative row and column
        with self.assertRaises(ValueError):
            self.logic.validate_board_boundaries(-1, 1)
        with self.assertRaises(ValueError):
            self.logic.validate_board_boundaries(1, -1)
        with self.assertRaises(ValueError):
            self.logic.validate_board_boundaries(-1, -1)

    def test_validate_board_boundaries_outside_ranges(self):
        # Test that the method raises an error for a row and column outside the board dimensions
        with self.assertRaises(ValueError):
            self.logic.validate_board_boundaries(3, 1)
        with self.assertRaises(ValueError):
            self.logic.validate_board_boundaries(1, 3)
        with self.assertRaises(ValueError):
            self.logic.validate_board_boundaries(3, 3)


if __name__ == '__main__':
    unittest.main()
