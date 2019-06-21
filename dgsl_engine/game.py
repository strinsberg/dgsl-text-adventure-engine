class Game:
    def __init__(self, world, parser, resolver, out=print, inp=input):
        self._in = inp
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
            result = self.resolver.resovle_input(parsed_input)
            self._out(result)

            if self._game_over():
                break

        self._cleanup()

    def _setup(self):
        pass

    def _cleanup(self):
        self._out("Thanks for playing")

    def _game_over(self):
        return self.world.player.states.hidden


class World:
    def __init__(self):
        self.name = "Untitled"
        self.welcome = "Welcome to my game!"
        self.opening = "You are in a very interesting place!"
        self.player_title = "Captain"
        self.version = "0.0.0"
        self.player = None
        self.entities = {}
        self.events = {}
