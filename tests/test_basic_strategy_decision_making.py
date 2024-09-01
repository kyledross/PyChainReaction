import unittest

from src.computer_logic import basic_strategy


class TestBasicStrategyDecisionMaking(unittest.TestCase):
    def test_best_move_one_choice(self):
        # board has player 1 in corner with 1 piece
        # player 2 in top middle with 2 pieces
        # player 2 could win by placing another piece in top middle, causing a reaction spilling into the corner
        # taking it from player 1 and ending the game
        board = [
        [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 0, 'num_pieces': 0}],
        [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
        [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}]
        ]

        result = basic_strategy.find_best_play(board, 2)
        self.assertEqual(
            result,
            (1, 0))

    def test_best_move_two_choices(self):
        # board has player 1 in upper-left corner with 1 piece
        # player 1 also has lower-right corner with 1 piece
        # player 2 in top middle with 2 pieces
        # player 2 should ignore lower-right corner and take the upper-left by playing top middle
        board = [
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 1, 'num_pieces': 1}]
        ]

        result = basic_strategy.find_best_play(board, 2)
        self.assertEqual(
            result,
            (1, 0))

    def test_best_move_two_choices_yield_same_result(self):
        # player 2 can add to lower-right corner or lower-middle
        # both cause chain reaction that takes lower-left corner from player 1
        board = [
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 2, 'num_pieces': 1}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}, {'player_id': 0, 'num_pieces': 0}],
            [{'player_id': 1, 'num_pieces': 1}, {'player_id': 2, 'num_pieces': 2}, {'player_id': 2, 'num_pieces': 1}]
        ]
        # todo: this is scoring bottom-middle higher than bottom-right, but they should both be equal, I think
        # figure out why
        result = basic_strategy.find_best_play(board, 2)
        self.assertEqual(
            result,
            (1, 0))


if __name__ == '__main__':
    unittest.main()
