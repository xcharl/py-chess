import unittest

from chess_logic import *


class BishopTests(unittest.TestCase):

    def setUp(self):
        self.board = ChessBoard(layout='blank')
        self.board_tiles = self.board.get_tiles()

    def test_get_moves_Bishop_Unblocked(self):
        expected_moves =\
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

        bishop = Bishop((0, 0), TeamColour.WHITE)
        board_tiles = self.board.get_tiles()
        board_tiles[0][0] = bishop
        avail_moves = bishop.get_moves(self.board)

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_Bishop_BlockedSameColour(self):
        expected_moves = [(1, 1), (2, 2), (3, 3)]

        bishop = Bishop((0, 0), TeamColour.WHITE)
        self.board_tiles[0][0] = bishop
        pawn = Pawn((4, 4), TeamColour.WHITE)
        self.board_tiles[4][4] = pawn

        avail_moves = bishop.get_moves(self.board)

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_Bishop_BlockedDifferentColour(self):
        expected_moves = [(1, 1), (2, 2), (3, 3), (4, 4)]

        bishop = Bishop((0, 0), TeamColour.WHITE)
        self.board_tiles[0][0] = bishop
        pawn = Pawn((4, 4), TeamColour.BLACK)
        self.board_tiles[4][4] = pawn

        avail_moves = bishop.get_moves(self.board)

        self.assertListEqual(expected_moves, avail_moves)


# class ChessBoardTests(unittest.TestCase):
#
#     def test_init_BoardSetUpCorrectly(self):
#         board = ChessBoard()
#         print('hello, joe')

if __name__ == '__main__':
    unittest.main()
