import copy
from abc import ABC, abstractmethod
from enum import Enum


class Colour(Enum):
    WHITE = 1
    BLACK = 2


class ChessBoard(object):

    def __init__(self, **kwargs):

        self.move_list = [7, 7, 7]

        # # Copy existing board
        # if kwargs.get('board') is not None:
        #     self.__tiles = copy.deepcopy(kwargs.get('board'))
        #     return

        # (row,col) with (0,0) in the top left.
        self.__tiles = []

        for i in range(0, 8):
            self.__tiles.append([])
            for j in range(0, 8):
                self.__tiles[i].append(None)

        # Blank board for unit testing
        if kwargs.get('layout', None) == 'blank':
            self.king_pos_dict = {
                Colour.WHITE: (-1, -1),
                Colour.BLACK: (-1, -1)}
            return

        # Standard new board
        self.__add_main_pieces(0, Colour.BLACK)
        self.__add_main_pieces(7, Colour.WHITE)
        self.__add_pawns()
        self.white_king_pos = (4, 0)
        self.black_king_pos = (4, 7)

    def get_tiles(self):
        return self.__tiles

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
            self.__add_piece('Pawn', (1, col), Colour.BLACK)
            self.__add_piece('Pawn', (6, col), Colour.WHITE)

    def __add_piece(self, class_name, pos, team):
        piece_class = globals()[class_name]
        piece = piece_class(pos, team)
        self.__tiles[pos[0]][pos[1]] = piece

    def is_in_check(self, colour):
        king_pos = self.king_pos_dict[colour]
        for x in range(0, 8):
            for y in range(0, 8):
                piece = self.__tiles[x][y]
                if piece is not None and piece.colour is not colour:
                    # prev_move not required for this method
                    moves = piece.get_moves(self,
                                            prev_move=((-1, -1), (-1, -1)))
                    if king_pos in moves:
                        return True
        return False

    def is_checkmate(self, colour):
        king_pos = self.king_pos_dict[colour]
        king = self.__tiles[king_pos[0]][king_pos[1]]
        return self.is_in_check(colour) and len(king.get_moves()) == 0


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

    def move(self, board, new_pos, **kwargs):
        """
        Move this piece to the designated new_pos, provided it is a valid move.

        :return: 'True' if piece has successfully moved, else 'False'.
        """
        if kwargs['prev_move'] is None:
            raise Exception()
        if new_pos in self.get_moves(board, prev_move=kwargs['prev_move']):
            tiles = board.get_tiles()
            tiles[self._position[0]][self._position[1]] = None
            tiles[new_pos[0]][new_pos[1]] = self
            self._position = new_pos
            return True
        return False

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
                    elif type(board_tiles[x][y]) is King:
                        # Pretend we can 'move through' an enemy king for
                        # determining if a piece is in check
                        pass
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

    def get_moves(self, board, **kwargs):
        avail_moves = []
        tiles = board.get_tiles()
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                new_x = self._position[0] + x
                new_y = self._position[1] + y

                if (self._is_cell_on_board((new_x, new_y))
                        and (x, y) != (0, 0)
                        and (tiles[new_x][new_y] is None
                             or tiles[new_x][new_y].colour != self.colour)
                        and not self.__is_pos_in_check(board, new_x, new_y)):
                    avail_moves.append((new_x, new_y))

        return avail_moves

    def __is_pos_in_check(self, board, x, y):
        new_board = copy.deepcopy(board)
        new_board.king_pos_dict[self.colour] = (x, y)
        return new_board.is_in_check(self.colour)

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
        self.__dir = 1 if team_colour == Colour.WHITE else -1
        self.__start_y = 1 if team_colour == Colour.WHITE else 6

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
        potential_moves = [(curr_x - 1, curr_y + self.__dir),
            (curr_x + 1, curr_y + self.__dir)]

        for move in potential_moves:
            tile = board_tiles[move[0]][move[1]]
            if tile is not None and tile.colour is not self.colour:
                avail_moves.append(move)

        return avail_moves

    def __get_forward_moves(self, board_tiles, curr_x, curr_y):
        avail_moves = []
        if board_tiles[curr_x][curr_y + self.__dir] is not None:
            return avail_moves

        avail_moves.append((curr_x, curr_y + self.__dir))
        if curr_y == self.__start_y \
                and board_tiles[curr_x][curr_y + (2 * self.__dir)] is None:
            avail_moves.append((curr_x, curr_y + (2 * self.__dir)))
        return avail_moves

    def __get_en_passant_moves(self, board_tiles, x, y, prev_move):
        avail_moves = []
        l_r = [(x + 1), (x - 1)]
        for x in l_r:
            # Check pawn is adjacent to current pawn, and if it has
            # only just moved into that square from the start line
            if (type(board_tiles[x][y]) is Pawn
                    and prev_move == ((x, y + (2 * self.__dir)), (x, y))):
                avail_moves.append((x, y + self.__dir))
        return avail_moves
