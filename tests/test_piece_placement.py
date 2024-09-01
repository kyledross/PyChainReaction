import unittest

from game_logic import logic


class TestLogic(unittest.TestCase):

    def setUp(self):
        self.logic = logic.Logic(logic.create_board(1, 1))


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
        self.assertFalse(self.logic.place_piece(0, 0, 2))
        self.assertEqual(self.logic.board[0][0]['player_id'], 1)

    def test_place_piece_on_empty_position(self):
        self.assertTrue(
            self.logic.place_piece(0, 0, 1))

if __name__ == '__main__':
    unittest.main()
