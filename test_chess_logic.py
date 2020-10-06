import unittest

from chess_logic import *


def add_piece(board, class_name, pos, colour):
    piece_class = globals()[class_name]
    piece = piece_class(pos, colour)
    board.get_tiles()[pos[0]][pos[1]] = piece
    if type(piece) is King:
        board.king_pos_dict[piece.colour] = pos
    return piece


class ChessBoardTests(unittest.TestCase):

    def setUp(self):
        self.board = ChessBoard(layout='blank')
        self.board_tiles = self.board.get_tiles()

    def test_move_piece_Normal(self):
        start_pos = (0, 0)
        new_pos = (7, 7)
        piece = add_piece(self.board, 'Bishop', start_pos, Colour.WHITE)
        success = self.board.move_piece(start_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[start_pos[0]][start_pos[1]])

    def test_is_in_check_WhiteInCheck(self):
        expected = True

        add_piece(self.board, 'King', (0, 0), Colour.WHITE)
        add_piece(self.board, 'Rook', (5, 0), Colour.BLACK)

        actual = self.board.is_in_check(Colour.WHITE)
        self.assertEqual(expected, actual)

    def test_is_in_check_BlackInCheck(self):
        expected = True

        add_piece(self.board, 'King', (7, 7), Colour.BLACK)
        add_piece(self.board, 'Bishop', (4, 4), Colour.WHITE)

        actual = self.board.is_in_check(Colour.BLACK)
        self.assertEqual(expected, actual)

    def test_is_in_check_NotCheck(self):
        expected = False

        add_piece(self.board, 'King', (1, 5), Colour.BLACK)
        add_piece(self.board, 'Bishop', (4, 4), Colour.WHITE)
        add_piece(self.board, 'Bishop', (4, 5), Colour.WHITE)

        actual = self.board.is_in_check(Colour.BLACK)
        self.assertEqual(expected, actual)

    def test_is_in_check_PawnChecked(self):
        # Pawns have some weird moves so I figured it
        # was worth including an extra test
        expected = True

        add_piece(self.board, 'King', (5, 5), Colour.BLACK)
        add_piece(self.board, 'Pawn', (4, 4), Colour.WHITE)

        actual = self.board.is_in_check(Colour.BLACK)
        self.assertEqual(expected, actual)

    # def test_is_in_check_Checkmate(self):
    #     pass
    #
    # def test_is_in_check_AvoidMateByTaking(self):
    #     pass


class ChessPieceTests(unittest.TestCase):

    def setUp(self):
        self.board = ChessBoard(layout='blank')
        self.board_tiles = self.board.get_tiles()


class KingTests(ChessPieceTests):

    def test_move_Normal(self):
        orig_pos, new_pos = (2, 0), (3, 1)
        piece = add_piece(self.board, 'King', orig_pos, Colour.WHITE)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[2][0])

    def test_move_InToCheck(self):
        orig_pos, new_pos = (2, 0), (3, 1)
        piece = add_piece(self.board, 'King', orig_pos, Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (3, 7), Colour.BLACK)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertFalse(success)
        self.assertEqual(piece, self.board_tiles[2][0])

    def test_move_TakePiece(self):
        orig_pos, new_pos = (2, 0), (3, 1)
        piece = add_piece(self.board, 'King', orig_pos, Colour.WHITE)
        _ = add_piece(self.board, 'Rook', new_pos, Colour.BLACK)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[2][0])

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(1, 0), (3, 0), (1, 1), (2, 1), (3, 1)])

        piece = add_piece(self.board, 'King', (2, 0), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedFile(self):
        expected_moves = sorted([(0, 1), (0, 3)])

        piece = add_piece(self.board, 'King', (0, 2), Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (1, 5), Colour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedBishops(self):
        expected_moves = sorted([(2, 1), (3, 1), (3, 2)])

        piece = add_piece(self.board, 'King', (2, 2), Colour.WHITE)
        _ = add_piece(self.board, 'Bishop', (5, 5), Colour.BLACK)
        _ = add_piece(self.board, 'Bishop', (5, 6), Colour.BLACK)
        _ = add_piece(self.board, 'Bishop', (5, 7), Colour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_TakePieceFromCheck(self):
        expected_moves = [(1, 6)]

        piece = add_piece(self.board, 'King', (0, 5), Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (0, 7), Colour.BLACK)
        _ = add_piece(self.board, 'Rook', (1, 6), Colour.BLACK)
        avail_moves = piece.get_moves(self.board)

        self.assertListEqual(expected_moves, avail_moves)


class BishopTests(ChessPieceTests):

    def test_move_Normal(self):
        orig_pos = (0, 0)
        new_pos = (7, 7)
        piece = add_piece(self.board, 'Bishop', orig_pos, Colour.WHITE)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[orig_pos[0]][orig_pos[1]])

    def test_move_Blocked(self):
        orig_pos = (0, 0)
        new_pos = (7, 7)
        piece = add_piece(self.board, 'Bishop', orig_pos, Colour.WHITE)
        _ = add_piece(self.board, 'Bishop', (4, 4), Colour.WHITE)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertFalse(success)
        self.assertIsNone(self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertEqual(self.board_tiles[orig_pos[0]][orig_pos[1]], piece)

    def test_move_InToCheck(self):
        orig_pos = (2, 0)
        new_pos = (3, 1)
        piece = add_piece(self.board, 'King', orig_pos, Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (3, 7), Colour.BLACK)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertFalse(success)
        self.assertEqual(piece, self.board_tiles[2][0])

    def test_get_moves_Unblocked1(self):
        expected_moves = sorted(
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])

        piece = add_piece(self.board, 'Bishop', (0, 0), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_Unblocked2(self):
        expected_moves = sorted(
            [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                (2, 0), (0, 2)])

        piece = add_piece(self.board, 'Bishop', (1, 1), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted([(1, 1), (2, 2), (3, 3)])

        piece = add_piece(self.board, 'Bishop', (0, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (4, 4), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted([(1, 1), (2, 2), (3, 3), (4, 4)])

        piece = add_piece(self.board, 'Bishop', (0, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (4, 4), Colour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class RookTests(ChessPieceTests):

    def test_move_Normal(self):
        orig_pos = (3, 6)
        new_pos = (3, 7)
        piece = add_piece(self.board, 'Rook', orig_pos, Colour.WHITE)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[orig_pos[0]][orig_pos[1]])

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = add_piece(self.board, 'Rook', (4, 0), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = add_piece(self.board, 'Rook', (4, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (4, 4), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = add_piece(self.board, 'Rook', (4, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (4, 4), Colour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class QueenTests(ChessPieceTests):

    def test_move_Normal(self):
        orig_pos = (0, 0)
        new_pos = (5, 5)
        piece = add_piece(self.board, 'Queen', orig_pos, Colour.WHITE)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[orig_pos[0]][orig_pos[1]])

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = add_piece(self.board, 'Rook', (4, 0), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = add_piece(self.board, 'Rook', (4, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (4, 4), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted(
            [(4, 1), (4, 2), (4, 3), (4, 4),
                (0, 0), (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0)])

        piece = add_piece(self.board, 'Rook', (4, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (4, 4), Colour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class KnightTests(ChessPieceTests):

    def test_move_Normal(self):
        orig_pos = (0, 0)
        new_pos = (1, 2)
        piece = add_piece(self.board, 'Knight', orig_pos, Colour.WHITE)
        success = self.board.move_piece(orig_pos, new_pos)

        self.assertTrue(success)
        self.assertEqual(piece, self.board_tiles[new_pos[0]][new_pos[1]])
        self.assertIsNone(self.board_tiles[orig_pos[0]][orig_pos[1]])

    def test_get_moves_Unblocked(self):
        expected_moves = sorted(
            [(1, 2), (1, 4), (2, 5), (4, 5), (5, 4), (5, 2), (4, 1), (2, 1)])

        piece = add_piece(self.board, 'Knight', (3, 3), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedSameColour(self):
        expected_moves = sorted([(2, 1)])

        piece = add_piece(self.board, 'Knight', (0, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (1, 2), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_BlockedDifferentColour(self):
        expected_moves = sorted([(1, 2), (2, 1)])

        piece = add_piece(self.board, 'Knight', (0, 0), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (1, 2), Colour.BLACK)
        avail_moves = sorted(piece.get_moves(self.board))

        self.assertListEqual(expected_moves, avail_moves)


class PawnTests(ChessPieceTests):

    def test_get_moves_White_CanTakeLeftOrRight(self):
        expected_move_1 = (3, 2)
        expected_move_2 = (5, 2)

        piece = add_piece(self.board, 'Pawn', (4, 1), Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (3, 2), Colour.BLACK)
        _ = add_piece(self.board, 'Rook', (5, 2), Colour.BLACK)
        avail_moves = piece.get_moves(self.board, prev_move=(-1, -1))

        self.assertIn(expected_move_1, avail_moves)
        self.assertIn(expected_move_2, avail_moves)

    def test_get_moves_Black_CanTakeLeftOrRight(self):
        expected_move_1 = (3, 5)
        expected_move_2 = (5, 5)

        piece = add_piece(self.board, 'Pawn', (4, 6), Colour.BLACK)
        _ = add_piece(self.board, 'Rook', (3, 5), Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (5, 5), Colour.WHITE)
        avail_moves = piece.get_moves(self.board, prev_move=(-1, -1))

        self.assertIn(expected_move_1, avail_moves)
        self.assertIn(expected_move_2, avail_moves)

    def test_get_moves_MoveForwardBlocked(self):
        piece_1 = add_piece(self.board, 'Pawn', (4, 1), Colour.WHITE)
        piece_2 = add_piece(self.board, 'Pawn', (6, 1), Colour.WHITE)

        _ = add_piece(self.board, 'Rook', (4, 2), Colour.WHITE)
        _ = add_piece(self.board, 'Rook', (6, 2), Colour.BLACK)

        avail_moves_1 = piece_1.get_moves(self.board, prev_move=(-1, -1))
        avail_moves_2 = piece_2.get_moves(self.board, prev_move=(-1, -1))

        self.assertEqual(len(avail_moves_1), 0)
        self.assertEqual(len(avail_moves_2), 0)

    def test_get_moves_MoveForward(self):
        expected_moves = sorted([(4, 2), (4, 3)])
        piece = add_piece(self.board, 'Pawn', (4, 1), Colour.WHITE)
        avail_moves = sorted(piece.get_moves(self.board, prev_move=(-1, -1)))
        self.assertListEqual(expected_moves, avail_moves)

    def test_get_moves_EnPassant(self):
        piece = add_piece(self.board, 'Pawn', (4, 4), Colour.WHITE)
        _ = add_piece(self.board, 'Pawn', (3, 4), Colour.BLACK)
        avail_moves = piece.get_moves(self.board, prev_move=((3, 6), (3, 4)))
        self.assertIn((3, 5), avail_moves)


if __name__ == '__main__':
    unittest.main()
