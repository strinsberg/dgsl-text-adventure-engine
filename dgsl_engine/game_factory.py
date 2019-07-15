"""Module for the game factory."""
import os
import json
import dgsl_engine.game as game
import dgsl_engine.user_input as user_input
import dgsl_engine.world as world
import dgsl_engine.actions as actions
import dgsl_engine.visitors as visitors


class GameFactory:
    """Creates a new game with some default components."""

    def new(self, world_name):
        """

        Args:
          world_name: 

        Returns:

        """
        parser = user_input.Parser()

        collector_factory = visitors.EntityCollectorFactory()
        menu_factory = user_input.MenuFactory()
        action_factory = actions.ActionFactory()
        resolver = actions.ActionResolver(collector_factory, menu_factory,
                                          action_factory)

        world_path = self._name_to_path(world_name)
        home = os.path.expanduser('~')
        file_path = os.path.join(home, ".dgsl/worlds", world_path)

        with open(file_path) as file:
            world_json = json.load(file)

        game_world = world.WorldFactory().new(world_json)

        return game.Game(game_world, parser, resolver)

    def _name_to_path(self, name):
        """

        Args:
          name: 

        Returns:

        """
        words = name.split()
        return "_".join(words) + ".world"
