"""Script to run the DGSL Application."""
import os
import site
from dgsl_engine.game_factory import GameFactory, name_to_path
from dgsl_engine.user_input import Menu

VERSION = '0.2.0'


def main():
    """Create and run a new game.

    Asks for a world name and uses game factory to build it.
    (Test world only for now)
    Then runs the game.
    """
    print("Welcome to the DGSL Text Adventure Engine")
    print(VERSION)
    print()

    choices = ["Play 'Disaster on the Good Ship Lethbridge'",
               'Load a custom World']
    menu = Menu(choices)
    idx = menu.ask()

    if idx == 0:
        world_name = "disaster on the good ship lethbridge"
    elif idx == 1:
        world_name = input("What world would you like to load? ")

    if idx < len(choices):
        world_path = os.path.join(
            site.USER_BASE, 'dgsl/worlds', name_to_path(world_name))

        if os.path.exists(world_path):
            game = GameFactory().new(world_path)
            game.run()
        else:
            print("That world does not exist!")

    else:
        print()
        print('Bye!')


if __name__ == '__main__':
    main()
