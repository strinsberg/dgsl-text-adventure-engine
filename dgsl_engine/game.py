from . import user_input
from . import commands


class Game:
    def __init__(self, world, parser, resolver, out=print, in_=input):
        self._in = in_
        self._out = out
        self.parser = parser
        self.world = world
        self.resolver = resolver
        self._setup()

    def run(self):
        """Main game loop.
        
        User specifies actions for the player to take and the result of
        those actions is passed to out (default print).
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
