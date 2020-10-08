
from enum import Enum
from random import Random
import os
import re

from chess_logic import ChessBoard, Colour, ChessRunner


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class GameType(Enum):
    MULTI_PLAYER = 1
    SINGLE_PLAYER = 2


class ChessConsoleManager:

    def run(self):
        io = ChessConsoleIO()
        runner = ChessRunner(io)
        runner.run()


class ChessConsoleIO:

    def __init__(self):
        self.__output = _ChessConsoleRenderer()
        self.__input = _ChessConsoleInput()

    def get_menu_input(self, options):
        """
        Gets valid input for a menu given a list of options.
        :param options: List of tuples (integer value, option text).
        :return: A valid menu integer.
        """
        self.__output.render_menu(options)
        valid_values = list(map(lambda opt: opt[0], options))
        return self.__input.get_menu_input(valid_values)

    def get_move_input(self):
        """
        Prompt user for input, validate format and return move coordinates.
        :return: A tuple of tuples with move coordinates
         ((old_x, old_y), (new_x, new_y))
        """
        return self.__input.get_move_input()

    def render_board(self, board):
        """
        Renders the chess board to the console.
        :param board: The board to render.
        """
        pass

    # def run(self):
    #     self.__print_menu_text()
    #     selected_input = input()
    #
    #     while not self.__is_valid_input(selected_input):
    #         print("Input is invalid, please enter a number:")
    #         selected_input = input()
    #
    #     if selected_input == '1':  # With a friend
    #         game_type = GameType.MULTI_PLAYER
    #     elif selected_input == '2':  # Against the computer
    #         game_type = GameType.SINGLE_PLAYER
    #     else:
    #         raise RuntimeError("'selected_input' not valid.")
    #
    #     runner = ChessConsoleRunner(game_type)
    #     runner.execute_game_loop()

    # def __print_menu_text(self):
    #     clear_console()
    #     print("Welcome to chess.")
    #     print("Would you like to play with a friend or against the computer?")
    #     print("1 With a friend")
    #     print("2 Against the computer")
    #     print("Please select a value:")
    #
    # def __is_valid_input(self, input_selected):
    #     return input_selected in self.__valid_menu_inputs


# class ChessConsoleRunner(object):
#
#     def __init__(self, game_type):
#         self.__game_type = game_type
#         self.__input = ChessConsoleInput()
#         self.__board = ChessBoard()
#         self.__renderer = ChessConsoleRenderer(self.__board)
#
#         # if game_type is GameType.MULTI_PLAYER:
#         #     self.__comp_player_id = -1
#         # elif game_type is GameType.SINGLE_PLAYER:
#         #     rng = Random()
#         #     self.__comp_player_id = rng.randint(1, 2)
#
#     def execute_game_loop(self):
#         winner = None
#         self.__renderer.render()
#         while True:
#             self.process_p1_turn()
#             self.__renderer.render()
#             if self.__board.is_checkmate(Colour.BLACK):
#                 winner = Colour.WHITE
#                 break
#
#             self.process_p2_turn()
#             self.__renderer.render()
#             if self.__board.is_checkmate(Colour.WHITE):
#                 winner = Colour.BLACK
#                 break
#
#     def process_p1_turn(self):
#         move = self.__input.get_parsed_input()
#         while not self.__board.move_piece(move[0], move[1]):
#             print('Invalid move')
#             move = self.__input.get_parsed_input()
#
#     def process_p2_turn(self):
#         pass


class _ChessConsoleRenderer(object):

    def render_board(self, board):
        clear_console()
        tiles = board.get_tiles()
        for y in range(7, -1, -1):
            line = str(y)
            line += " |"
            for x in range(0, 8):
                line += tiles[y][x].get_letter_representation() + "|"\
                    if tiles[y][x] is not None \
                    else " |"

            print(line)

    def render_menu(self, options):
        string_opts = map(lambda opt: str(opt[0]) + ') ' + opt[1], options)
        output = '\n'.join(string_opts) + '\n'
        print(output)


class _ChessConsoleInput(object):

    def get_menu_input(self, valid_values):
        raw_input = input()
        while not self.__is_menu_input_valid(raw_input, valid_values):
            print('Please select a numeric option from the menu.\n')
            raw_input = input()
        return int(raw_input)

    def __is_menu_input_valid(self, raw_input, valid_values):
        if self.__is_int(raw_input) and int(raw_input) in valid_values:
            return True
        else:
            return False

    def __is_int(self, raw_input):
        try:
            _ = int(raw_input)
            return True
        except ValueError:
            return False

    def get_move_input(self):
        player_input = self.__get_valid_move_input()
        return self.__parse_move_input(player_input)

    def __get_valid_move_input(self):
        raw_input = self.__get_raw_move_input().lower()
        while not self.__is_move_input_valid(raw_input):
            raw_input = self.__get_raw_move_input()
        return raw_input

    def __get_raw_move_input(self):
        print("Please enter your move in the format 'e2 e4': ")
        return input()

    def __is_move_input_valid(self, raw_input):
        return re.match('[a-h][1-8] [a-h][1-8]', raw_input)

    def __parse_move_input(self, player_input):
        x0 = int(self.__get_num_from_char(player_input[0]))
        y0 = int(player_input[1]) - 1
        x1 = int(self.__get_num_from_char(player_input[3]))
        y1 = int(player_input[4]) - 1
        return (x0, y0), (x1, y1)

    def __get_num_from_char(self, letter):
        return ord(letter) - 97


if __name__ == '__main__':
    manager = ChessConsoleManager()
    manager.run()
