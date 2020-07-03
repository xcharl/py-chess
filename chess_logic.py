from abc import ABC, abstractmethod
from enum import Enum


class TeamColour(Enum):
    WHITE = 1
    BLACK = 2


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class ChessBoard(object):

    def __init__(self, **kwargs):

        # (row,col) with (0,0) in the top left.
        self.__board = []

        for i in range(0, 8):
            self.__board.append([])
            for j in range(0, 8):
                self.__board[i].append(None)

        # Blank board for unit testing
        if kwargs.get('layout', None) == 'blank':
            return

        self.__add_main_pieces(0, TeamColour.BLACK)
        self.__add_main_pieces(7, TeamColour.WHITE)
        self.__add_pawns()

    def get_tiles(self):
        return self.__board

    def __add_main_pieces(self, row, team):
        self.__add_piece('Rook', (row, 0), team)
        self.__add_piece('Rook', (row, 7), team)
        self.__add_piece('Knight', (row, 1), team)
        self.__add_piece('Knight', (row, 6), team)
        self.__add_piece('Bishop', (row, 2), team)
        self.__add_piece('Bishop', (row, 5), team)
        self.__add_piece('Queen', (row, 3), team)
        self.__add_piece('King', (row, 4), team)

    def __add_pawns(self):
        for col in range(0, 8):
            self.__add_piece('Pawn', (1, col), TeamColour.BLACK)
            self.__add_piece('Pawn', (6, col), TeamColour.WHITE)

    def __add_piece(self, class_name, pos, team):
        piece_class = globals()[class_name]
        piece = piece_class(pos, team)
        self.__board[pos[0]][pos[1]] = piece


class ChessPiece(ABC):

    def __init__(self, position, team_colour):
        self.colour = team_colour
        self._position = position
        pass

    @abstractmethod
    def get_letter_representation(self):
        pass

    @abstractmethod
    def get_moves(self, board):
        """
        Uses position to get all available squares the piece can move to.

        # Returns
            List of (x,y) coordinate tuples.
        """
        pass

    def get_position(self):
        return self._position

    def _get_diagonal_moves(self, board):
        diagonal_vectors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        board_tiles = board.get_tiles()
        return self.__get_moves_from_vectors(board_tiles, diagonal_vectors)

    def _get_orthogonal_moves(self, board):
        orthogonal_vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        board_tiles = board.get_tiles()
        return self.__get_moves_from_vectors(board_tiles, orthogonal_vectors)

    def __get_moves_from_vectors(self, board_tiles, vectors):
        available_moves = []
        for vector in vectors:
            curr_cell = self.__step(self._position, vector)
            while self.__is_cell_on_board(curr_cell):
                x = curr_cell[0]
                y = curr_cell[1]
                if board_tiles[x][y] is not None:  # Piece in this position
                    if board_tiles[x][y].colour is self.colour:
                        # Can't move into your own piece
                        break
                    else:
                        # Can capture enemy piece
                        available_moves.append(curr_cell)
                        break
                available_moves.append(curr_cell)
                curr_cell = self.__step(curr_cell, vector)
        return available_moves

    def __step(self, cell, vector):
        return cell[0] + vector[0], cell[1] + vector[1]

    def __is_cell_on_board(self, cell):
        return 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7


class King(ChessPiece):

    def __init__(self, position, team_colour):
        super().__init__(position, team_colour)
        self.is_in_check = False

    def get_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'K'


class Queen(ChessPiece):
    def get_moves(self, board: ChessBoard):
        diagonal_moves = self._get_diagonal_moves(board)
        orthogonal_moves = self._get_orthogonal_moves(board)
        return orthogonal_moves + diagonal_moves

    def get_letter_representation(self):
        return 'Q'


class Rook(ChessPiece):
    def get_moves(self, board: ChessBoard):
        return self._get_orthogonal_moves(board)
        pass

    def get_letter_representation(self):
        return 'R'


class Bishop(ChessPiece):
    def get_moves(self, board: ChessBoard):
        return self._get_diagonal_moves(board)

    def get_letter_representation(self):
        return 'B'


class Knight(ChessPiece):
    def get_moves(self, board: ChessBoard):

        pass

    def get_letter_representation(self):
        return 'N'


class Pawn(ChessPiece):
    def get_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'P'
