import unittest

from game_logic.logic import Logic


class TestGamePlay(unittest.TestCase):
    def test_gameplay(self):
        self.board = [[{'player_id': 0, 'num_pieces': 0} for _ in range(3)] for _ in range(3)]
        game = Logic(self.board)

        game.place_piece(0, 0, 1)
        game.process_board()
        self.assertEqual(game.winner_determined(), False)

        game.place_piece(0, 1, 2)
        game.process_board()
        self.assertEqual(game.winner_determined(), False)

        game.place_piece(0, 0, 1)
        winner_detected: bool = game.process_board()
        self.assertEqual(game.winner_determined(), True)
        self.assertEqual(winner_detected, True)

    def test_full_board_flip(self):
        self.board = [[{'player_id': 0, 'num_pieces': 0} for _ in range(3)] for _ in range(3)]
        game = Logic(self.board)

        # row 0 ----------------------------------------------------
        # player 1 has 1 corner piece
        game.place_piece(0, 0, 1)

        # player 2 has 2 edge pieces
        game.place_piece(0, 1, 2)
        game.place_piece(0, 1, 2)

        # player 2 has 1 corner piece
        game.place_piece(0, 2, 2)

        # row 2 ----------------------------------------------------
        # player 2 has two left edge pieces
        game.place_piece(1, 0, 2)
        game.place_piece(1, 0, 2)

        # player 2 has three middle pieces
        game.place_piece(1, 1, 2)
        game.place_piece(1, 1, 2)
        game.place_piece(1, 1, 2)

        # player 2 has two right edge pieces
        game.place_piece(1, 2, 2)
        game.place_piece(1, 2, 2)

        # row 3 ----------------------------------------------------
        # player 2 has 1 corner piece
        game.place_piece(2, 0, 2)

        # player 2 has 2 edge pieces
        game.place_piece(2, 1, 2)
        game.place_piece(2, 1, 2)

        # player 3 has 1 corner piece
        game.place_piece(2, 2, 2)

        win_detected = game.process_board()
        self.assertEqual(win_detected, False)

        # player 1 places piece into top left corner,
        # causing a cascade that takes over the board and wins
        game.place_piece(0, 0, 1)
        win_detected = game.process_board()
        self.assertEqual(win_detected, True)


if __name__ == '__main__':
    unittest.main()
