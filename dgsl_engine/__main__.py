"""Script to run the DGSL Application."""
import os
from dgsl_engine.game_factory import GameFactory, name_to_path
from dgsl_engine.user_input import Menu

VERSION = 0.1
DGSL_DIR = os.path.join(os.path.expanduser('~'), '.dgsl')


def main():
    """Create and run a new game.

    Asks for a world name and uses game factory to build it.
    (Test world only for now)
    Then runs the game.
    """
    print("Welcome to the DGSL Text Adventure Engine")
    print(VERSION)
    print()

    menu = Menu(['Load a world', 'Load a saved game (not implemented)'])
    idx = menu.ask()

    if idx == 0:
        world_name = input("What world would you like to load? ")
        world_path = os.path.join(
            DGSL_DIR, 'worlds', name_to_path(world_name))

        if os.path.exists(world_path):
            game = GameFactory().new(world_path)
            game.run()
        else:
            print("That world does not exist!")

    else:
        print()
        print('See you soon!')
