import sys
import unittest
import io

from chess_console import ChessConsoleIO
from unittest.mock import patch

from chess_logic import ChessBoard


class ChessConsoleIOTests(unittest.TestCase):

    def setUp(self):
        self.io = ChessConsoleIO()  # Class Under Test
        self.captured_output = io.StringIO()
        self.orig_stdout = sys.stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = self.orig_stdout

    def _assertOutput(self, expected):
        """
        Asserts that the output to stdout equals the expected value.
        :param expected: Value expected in stdout.
        """
        actual = self.captured_output.getvalue()
        self.assertEqual(expected, actual)

    def test_get_menu_input_Happy(self):
        with patch('builtins.input', return_value='1'):
            options = [(1, "Hello"), (2, "Goodbye")]
            expected_val = 1
            actual_val = self.io.get_menu_input(options)
            self.assertEqual(expected_val, actual_val)

            expected_out = '1) Hello\n2) Goodbye\n\n'
            self._assertOutput(expected_out)

    def test_get_menu_input_InvalidInputFirst(self):
        with patch('builtins.input', side_effect=['3', '2']):
            options = [(1, "Hello"), (2, "Goodbye")]

            expected_val = 2
            actual_val = self.io.get_menu_input(options)
            self.assertEqual(expected_val, actual_val)

            expected_out = '1) Hello\n2) Goodbye\n\nPlease select a ' \
                           'numeric option from the menu.\n\n'
            self._assertOutput(expected_out)

    def test_get_move_input_Happy(self):
        with patch('builtins.input', return_value='b1 h7'):
            parsed_input = self.io.get_move_input()
            self.assertEqual(((1, 0), (7, 6)), parsed_input)

    def test_get_move_input_InvalidInputFirst(self):
        with patch('builtins.input', side_effect=['e2 99', 'e2 e4']) \
                as mock_input:
            parsed_input = self.io.get_move_input()
            self.assertEqual(((4, 1), (4, 3)), parsed_input)
            self.assertEqual(2, mock_input.call_count)


if __name__ == '__main__':
    unittest.main()
