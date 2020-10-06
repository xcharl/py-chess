import unittest

from chess_console import ChessConsoleInput
from unittest.mock import patch


class ChessConsoleInputTests(unittest.TestCase):

    def setUp(self):
        self.input = ChessConsoleInput()  # Class Under Test

    def test_get_parsed_input_Happy(self):
        with patch('builtins.input', return_value='b1 h7'):
            parsed_input = self.input.get_parsed_input()
            self.assertEqual(((1, 0), (7, 6)), parsed_input)

    def test_get_parsed_input_InvalidInputFirst(self):
        with patch('builtins.input', side_effect=['e2 99', 'e2 e4']) as mock_input:
            parsed_input = self.input.get_parsed_input()
            self.assertEqual(((4, 1), (4, 3)), parsed_input)
            self.assertEqual(2, mock_input.call_count)


if __name__ == '__main__':
    unittest.main()
