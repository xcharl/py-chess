import unittest

from chess_logic import *


class BishopTests(unittest.TestCase):

    def test_get_available_moves_ProvidesCorrectMoves(self):
        expected_moves =\
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

        board = ChessBoard(layout='blank')
        bishop = Bishop((0, 0), TeamColour.WHITE)
        board[(0, 0)] = bishop

        avail_moves = bishop.get_available_moves(board)

        self.assertListEqual(expected_moves, avail_moves)


# class ChessBoardTests(unittest.TestCase):
#
#     def test_init_BoardSetUpCorrectly(self):
#         board = ChessBoard()
#         print('hello, joe')
