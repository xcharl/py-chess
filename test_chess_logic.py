import unittest

from chess_logic import *


class ChessPieceTests(unittest.TestCase):

    def setUp(self):
        self.board = ChessBoard(layout='blank')
        self.board_tiles = self.board.get_tiles()

    def add_piece(self, class_name, pos, colour):
        piece_class = globals()[class_name]
        piece = piece_class(pos, colour)
        self.board_tiles[pos[0]][pos[1]] = piece
        return piece


class BishopTests(ChessPieceTests):

    def test_get_moves_Unblocked1(self):
        expected_moves = sorted(
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])

        piece = self.add_piece('Bishop', (0, 0), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_Unblocked2(self):
        expected_moves = sorted(
            [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                (2, 0), (0, 2)])

        piece = self.add_piece('Bishop', (1, 1), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted([(1, 1), (2, 2), (3, 3)])

        piece = self.add_piece('Bishop', (0, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (4, 4), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted([(1, 1), (2, 2), (3, 3), (4, 4)])

        piece = self.add_piece('Bishop', (0, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (4, 4), TeamColour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class RookTests(ChessPieceTests):

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = self.add_piece('Rook', (4, 0), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = self.add_piece('Rook', (4, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (4, 4), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = self.add_piece('Rook', (4, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (4, 4), TeamColour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class QueenTests(ChessPieceTests):

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = self.add_piece('Rook', (4, 0), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = self.add_piece('Rook', (4, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (4, 4), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = self.add_piece('Rook', (4, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (4, 4), TeamColour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class KnightTests(ChessPieceTests):

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(1, 2), (1, 4), (2, 5), (4, 5), (5, 4), (5, 2), (4, 1), (2, 1)])

        piece = self.add_piece('Knight', (3, 3), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted([(2, 1)])

        piece = self.add_piece('Knight', (0, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (1, 2), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted([(1, 2), (2, 1)])

        piece = self.add_piece('Knight', (0, 0), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (1, 2), TeamColour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class PawnTests(ChessPieceTests):

    def test_get_moves_White_CanTakeLeftOrRight(self):
        expected_move_1 = (3, 2)
        expected_move_2 = (5, 2)

        piece = self.add_piece('Pawn', (4, 1), TeamColour.WHITE)
        _ = self.add_piece('Rook', (3, 2), TeamColour.BLACK)
        _ = self.add_piece('Rook', (5, 2), TeamColour.BLACK)
        avail_moves = piece.get_moves(self.board)

        self.assertIn(expected_move_1, avail_moves)
        self.assertIn(expected_move_2, avail_moves)

    def test_get_moves_Black_CanTakeLeftOrRight(self):
        expected_move_1 = (3, 5)
        expected_move_2 = (5, 5)

        piece = self.add_piece('Pawn', (4, 6), TeamColour.BLACK)
        _ = self.add_piece('Rook', (3, 5), TeamColour.WHITE)
        _ = self.add_piece('Rook', (5, 5), TeamColour.WHITE)
        avail_moves = piece.get_moves(self.board, prev_move=(-1, -1))

        self.assertIn(expected_move_1, avail_moves)
        self.assertIn(expected_move_2, avail_moves)

    def test_get_moves_MoveForwardBlocked(self):
        piece_1 = self.add_piece('Pawn', (4, 1), TeamColour.WHITE)
        piece_2 = self.add_piece('Pawn', (6, 1), TeamColour.WHITE)

        _ = self.add_piece('Rook', (4, 2), TeamColour.WHITE)
        _ = self.add_piece('Rook', (6, 2), TeamColour.BLACK)

        avail_moves_1 = piece_1.get_moves(self.board, prev_move=(-1, -1))
        avail_moves_2 = piece_2.get_moves(self.board, prev_move=(-1, -1))

        self.assertEqual(len(avail_moves_1), 0)
        self.assertEqual(len(avail_moves_2), 0)

    def test_get_moves_MoveForward(self):
        expected_moves = sorted([(4, 2), (4, 3)])
        piece = self.add_piece('Pawn', (4, 1), TeamColour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board, prev_move=(-1, -1)))
        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_EnPassant(self):
        expected_move = (3, 3)
        piece = self.add_piece('Pawn', (4, 4), TeamColour.WHITE)
        _ = self.add_piece('Pawn', (3, 4), TeamColour.BLACK)
        avail_moves = piece.get_moves(self.board, prev_move=(3, 4))


if __name__ == '__main__':
    unittest.main()
