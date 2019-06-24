"""Script to run the DGSL Application."""
from dgsl_engine.game_factory import GameFactory


def main():
    """Create and run a new game.

    Asks for a world name and uses game factory to build it.
    (Test world only for now)
    Then runs the game.
    """
    world_name = 'testing ground'
    game = GameFactory().new(world_name)
    game.run()


if __name__ == '__main__':
    main()
