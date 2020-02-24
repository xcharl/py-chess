from abc import ABC, abstractmethod
from enum import Enum


class TeamColour(Enum):
    WHITE = 1
    BLACK = 2


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

    def __getitem__(self, coord):
        return self.__board[coord[0]][coord[1]]

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
        self._position = position
        self._team = team_colour
        pass

    @abstractmethod
    def get_letter_representation(self):
        pass

    @abstractmethod
    def get_available_moves(self, board: ChessBoard):
        """
        Uses position to get all available squares the piece can move to.

        # Returns
            List of (x,y) coordinate tuples.
        """
        pass

    def get_position(self):
        return self._position

    def _get_diagonal_moves(self, board_tiles):

        def step_SE(cell):
            curr_cell[0] += 1
            curr_cell[0] += 1

        available_moves = []
        curr_cell = self._position
        # NE

        # SE
        step_SE(curr_cell)
        while self.__is_cell_on_board(curr_cell):

            if board_tiles[curr_cell[0], curr_cell[1]] is not None:
                pass

            # if it contains a piece of same colour, stop
            # if it contains a piece of opposing colour, add to list and stop
        # SW
        # NW

    def __is_cell_on_board(self, cell):
        return 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7

    # @abstractmethod
    # def get_available_moves(self):
    #     pass


class King(ChessPiece):

    def __init__(self, position, team_colour):
        super().__init__(position, team_colour)
        self.is_in_check = False

    def get_available_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'K'


class Queen(ChessPiece):
    def get_available_moves(self, board: ChessBoard):
        diagonal_moves = self._get_diagonal_moves(board)

        pass

    def get_letter_representation(self):
        return 'Q'


class Rook(ChessPiece):
    def get_available_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'R'


class Bishop(ChessPiece):
    def get_available_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'B'


class Knight(ChessPiece):
    def get_available_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'N'


class Pawn(ChessPiece):
    def get_available_moves(self, board: ChessBoard):
        pass

    def get_letter_representation(self):
        return 'P'
