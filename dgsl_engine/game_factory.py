"""Module for the game factory."""
import json
import dgsl_engine.game as game
import dgsl_engine.user_input as user_input
import dgsl_engine.world as world
import dgsl_engine.actions as actions
import dgsl_engine.collectors as collectors


class GameFactory:  # pylint: disable=too-few-public-methods
    """Creates a new game with some default components."""

    def new(self, world_path):  # pylint: disable=no-self-use
        """Creates a new game with default components.

        Args:
          world_path (str): The path to the world for the game.

        Returns:
            Game: The newly created game.
        """
        parser = user_input.Parser()

        collector_factory = collectors.EntityCollectorFactory()
        menu_factory = user_input.MenuFactory()
        action_factory = actions.ActionFactory()
        resolver = actions.ActionResolver(collector_factory, menu_factory,
                                          action_factory)

        with open(world_path) as file:
            world_json = json.load(file)

        game_world = world.WorldFactory().new(world_json)

        return game.Game(game_world, parser, resolver)


def name_to_path(name):
    """Turns a world name into a path ending with .world.

    Args:
        name (str): The name to convert.

    Returns:
        str: The new path.
    """
    words = name.split()
    return "_".join(words) + ".world"
