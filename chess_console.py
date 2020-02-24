from chess_common import Point
from enum import Enum
from random import Random
import os
import re


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class GameType(Enum):
    MULTI_PLAYER = 1
    SINGLE_PLAYER = 2


class ChessConsoleManager(object):

    def __init__(self):
        self.__valid_menu_inputs = ["1", "2"]

    def run(self):
        self.print_menu_text()
        selected_input = input()

        while not self.is_valid_input(selected_input):
            print("Input is invalid, please enter a number:")
            selected_input = input()

        if selected_input == '1':  # With a friend
            game_type = GameType.MULTI_PLAYER
        elif selected_input == '2':  # Against the computer
            game_type = GameType.SINGLE_PLAYER
        else:
            raise RuntimeError("'selected_input' not valid.")

        runner = ChessConsoleRunner(game_type)
        runner.execute_game_loop()

    def print_menu_text(self):
        clear_console()
        print("Welcome to chess.")
        print("Would you like to play with a friend or against the computer?")
        print("1 With a friend")
        print("2 Against the computer")
        print("Please select a value:")

    def is_valid_input(self, input_selected):
        return input_selected in self.__valid_menu_inputs


class ChessConsoleRunner(object):

    def __init__(self, game_type):
        self.__game_type = game_type
        self.__renderer = ChessConsoleRenderer()

        if game_type is GameType.MULTI_PLAYER:
            self.__comp_player_id = -1
        elif game_type is GameType.SINGLE_PLAYER:
            rng = Random()
            self.__comp_player_id = rng.randint(1, 2)

    def execute_game_loop(self):
        # game_over = False
        while True:
            self.process_p1_turn()
            self.process_p2_turn()
            pass

    def process_p1_turn(self):
        pass

    def process_p2_turn(self):
        pass


class ChessConsoleRenderer(object):
    pass


class ChessConsoleInput(object):

    def get_parsed_input(self):
        player_input = self.__get_valid_input()
        return self.__parse_input(player_input)

    def __parse_input(self, player_input):
        x0 = int(self.__get_num_from_char(player_input[0]))
        y0 = int(player_input[1]) - 1
        x1 = int(self.__get_num_from_char(player_input[3]))
        y1 = int(player_input[4]) - 1
        return Point(x0, y0), Point(x1, y1)

    def __get_num_from_char(self, letter):
        return ord(letter) - 97

    def __get_valid_input(self):
        raw_input = self.__get_input().lower()
        while not self.__is_input_valid(raw_input):
            raw_input = self.__get_input()
        return raw_input

    def __get_input(self):
        print("Please enter your move in the format 'e2 e4': ")
        return input()

    def __is_input_valid(self, raw_input):
        return re.match('[a-h][1-8] [a-h][1-8]', raw_input)