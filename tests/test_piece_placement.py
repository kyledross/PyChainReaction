import unittest

import logic
from GameLogic.logic import Logic


class TestLogic(unittest.TestCase):

    def setUp(self):
        self.logic = Logic(logic.create_board(1,1))


    def test_place_piece_increase_num_pieces(self):
        initial_num_pieces = self.logic.board[0][0]['num_pieces']
        self.logic.place_piece(0, 0, 1)
        self.assertEqual(self.logic.board[0][0]['num_pieces'], initial_num_pieces + 1)

    def test_place_piece_assigns_player_id(self):
        player_id = 1
        self.logic.place_piece(0, 0, player_id)
        self.assertEqual(self.logic.board[0][0]['player_id'], player_id)

    def test_place_piece_on_occupied_position(self):
        player_id = 1
        self.logic.place_piece(0, 0, player_id)
        initial_num_pieces = self.logic.board[0][0]['num_pieces']
        self.logic.place_piece(0, 0, player_id)
        self.assertEqual(self.logic.board[0][0]['num_pieces'], initial_num_pieces + 1)

    def test_place_piece_on_occupied_by_another_player_position(self):
        player_id = 1
        self.logic.place_piece(0, 0, player_id)
        self.logic.place_piece(0, 0, 2)
        self.assertEqual(self.logic.board[0][0]['player_id'], 2)


if __name__ == '__main__':
    unittest.main()
