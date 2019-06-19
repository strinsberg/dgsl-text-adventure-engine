from . import actions
from . import user_input
from . import entity_containers as containers


class Game:
    def __init__(self, parser, out=print, inp=input):
        self._in = inp
        self._out = out
        self.parser = parser
        self.world = None
        self._setup()

    def run(self):
        """Main game loop.
        
        User specifies actions for the player to take and the result of
        those actions is passed to out (default print).
        """
        self.world.player.spec.name = self._opening()

        while True:
            raw_input = self._in("> ")
            parsed_input = self.parser.parse(raw_input)

            if parsed_input['code'] is not None:
                done = self._handle_code(parsed_input)
            else:
                self._out(actions.take_action(parsed_input, self.world))

            if self._finished() or done:
                self._out("Thanks for playing")  # add cleanup if necessary
                break

    def _setup(self):
        # Eventually replace with some code that builds things
        # parser can be given grammer if thats necessary
        self.world = World()
        self.world.player = containers.Player("Bogus ID")

    def _opening(self):
        self._out(self.world.name)
        self._out(self.world.version)
        self._out()
        self._out(self.world.welcome)
        self._out()
        name = self._in("What is your name? ")
        self._out()
        self._out()
        self._out("Welcome " + self.world.player_title + " " + name)
        self._out()
        self._out(self.world.opening)
        self._out()
        return name

    def _handle_code(self, parsed):
        if parsed['code'] == user_input.ParseCodes.BAD_VERB:
            self._out(parsed['message'])
        elif parsed['code'] == user_input.ParseCodes.COMMAND:
            return True

        return False

    def _finished(self):
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
