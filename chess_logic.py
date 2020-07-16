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

    @abstractmethod
    def get_letter_representation(self):
        pass

    @abstractmethod
    def get_moves(self, board, **kwargs):
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

    def _get_cell_from_vector(self, cell, vector):
        return cell[0] + vector[0], cell[1] + vector[1]

    def __get_moves_from_vectors(self, board_tiles, vectors):
        available_moves = []
        for vector in vectors:
            curr_cell = self._get_cell_from_vector(self._position, vector)
            while self._is_cell_on_board(curr_cell):
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
                curr_cell = self._get_cell_from_vector(curr_cell, vector)
        return available_moves

    def _is_cell_on_board(self, cell):
        return 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7


class King(ChessPiece):

    def __init__(self, position, team_colour):
        super().__init__(position, team_colour)
        self.is_in_check = False

    def get_moves(self, board, **kwargs):
        pass

    def get_letter_representation(self):
        return 'K'


class Queen(ChessPiece):
    def get_moves(self, board, **kwargs):
        diagonal_moves = self._get_diagonal_moves(board)
        orthogonal_moves = self._get_orthogonal_moves(board)
        return orthogonal_moves + diagonal_moves

    def get_letter_representation(self):
        return 'Q'


class Rook(ChessPiece):
    def get_moves(self, board, **kwargs):
        return self._get_orthogonal_moves(board)
        pass

    def get_letter_representation(self):
        return 'R'


class Bishop(ChessPiece):
    def get_moves(self, board, **kwargs):
        return self._get_diagonal_moves(board)

    def get_letter_representation(self):
        return 'B'


class Knight(ChessPiece):
    def get_moves(self, board, **kwargs):
        available_moves = []
        knight_vectors = \
            [(1, 2), (-1, 2), (1, -2), (-1, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)]

        board_tiles = board.get_tiles()
        potential_moves = [
            self._get_cell_from_vector(self._position, v)
            for v in knight_vectors]
        for move in potential_moves:
            if not self._is_cell_on_board(move):
                continue
            board_tile = board_tiles[move[0]][move[1]]
            if board_tile is not None and board_tile.colour is self.colour:
                # Can't move to this tile if occupied by one of your pieces
                continue
            available_moves.append(move)

        return available_moves

    def get_letter_representation(self):
        return 'N'


class Pawn(ChessPiece):
    def __init__(self, position, team_colour):
        super().__init__(position, team_colour)
        self.__dir = 1 if team_colour == TeamColour.WHITE else -1

    def get_moves(self, board, **kwargs):
        if kwargs['prev_move'] is None:
            raise Exception()

        avail_moves = []
        board_tiles = board.get_tiles()
        curr_x, curr_y = self._position[0], self._position[1]

        avail_moves += self.__get_l_r_moves(board_tiles, curr_x, curr_y)
        avail_moves += self.__get_forward_moves(board_tiles, curr_x, curr_y)
        avail_moves += self.__get_en_passant_moves(
            board_tiles, curr_x, curr_y, kwargs['prev_move'])
        return avail_moves

    def get_letter_representation(self):
        return 'P'

    def __get_l_r_moves(self, board_tiles, curr_x, curr_y):
        avail_moves = []
        if self.colour == TeamColour.WHITE:
            potential_moves = [(curr_x - 1, curr_y + 1),
                (curr_x + 1, curr_y + 1)]
        else:
            potential_moves = [(curr_x - 1, curr_y - 1),
                (curr_x + 1, curr_y - 1)]

        for move in potential_moves:
            tile = board_tiles[move[0]][move[1]]
            if tile is not None and tile.colour is not self.colour:
                avail_moves.append(move)

        return avail_moves

    def __get_forward_moves(self, board_tiles, curr_x, curr_y):
        avail_moves = []
        if self.colour == TeamColour.WHITE:
            if board_tiles[curr_x][curr_y + 1] is None:
                avail_moves.append((curr_x, curr_y + 1))
            if curr_y == 1 and board_tiles[curr_x][curr_y + 2] is None:
                avail_moves.append((curr_x, curr_y + 2))
        else:
            if board_tiles[curr_x][curr_y - 1] is None:
                avail_moves.append((curr_x, curr_y - 1))
            if curr_y == 6 and board_tiles[curr_x][curr_y - 2] is None:
                avail_moves.append((curr_x, curr_y - 2))

    def __get_en_passant_moves(self, board_tiles, curr_x, curr_y, prev_move):
        avail_moves = []
        if self.colour == TeamColour.WHITE:
            if curr_y != 4:
                return avail_moves
            if

            potential_moves = [(curr_x - 1, curr_y + 1),
                (curr_x + 1, curr_y + 1)]
            if
        else:
            potential_moves = [(curr_x - 1, curr_y - 1),
                (curr_x + 1, curr_y - 1)]

        if self.colour == TeamColour.WHITE:
            if
