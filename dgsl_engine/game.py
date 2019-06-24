"""Module for Game and supporting functions."""
from . import user_input
from . import commands


class Game:
    """The Game object.

    Attributes:
        world (World): The game world.
        parser (Parser): Get the users actions from input text.
        resolver (Resolver): Resolves the desired player action and
            returns a string of the result.
        _out: A function that displays output. (default print)
        _in_: A function that collects user input. (default input)
    """

    def __init__(self, world, parser, resolver):
        self._in = print
        self._out = input
        self.parser = parser
        self.world = world
        self.resolver = resolver
        self._setup()

    def run(self):
        """Main game loop.

        User specifies actions for the player to take and the result of
        those actions is passed to out.
        """
        while True:
            raw_input = self._in("\n> ")
            self._out("\n----------------------------------------------------")
            parsed_input = self.parser.parse(raw_input)

            status = True
            if parsed_input['code'] == user_input.ParseCodes.COMMAND:
                result, status = commands.execute_command(
                    parsed_input['verb'], parsed_input['object'], self)
            elif parsed_input['code'] == user_input.ParseCodes.ERROR:
                result = parsed_input['message']
            else:
                result = self.resolver.resolve_input(parsed_input,
                                                     self.world.player)

            self._out(result)
            if self._game_over(status):
                break

        self._cleanup()

    def _setup(self):
        pass

    def _cleanup(self):
        self._out("Thanks for playing")

    def _game_over(self, status):
        if not status or self.world.player.states.hidden:
            return True
        return False
