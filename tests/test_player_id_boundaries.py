# File: test_player_id_boundaries.py
import unittest

from src.game_logic import logic


class TestLogic(unittest.TestCase):
    def test_validate_player_id(self):
        # Test with valid player_id
        try:
            logic.validate_player_id(1)
            logic.validate_player_id(2)
        except ValueError:
            self.fail("validate_player_id raises ValueError unexpectedly!")

        # Test with invalid player_id
        with self.assertRaises(ValueError):
            logic.validate_player_id(3)

        with self.assertRaises(ValueError):
            logic.validate_player_id(-1)

        with self.assertRaises(ValueError):
            logic.validate_player_id(0)


if __name__ == "__main__":
    unittest.main()
