class Game:
    def __init__(self, out=print):
        self.out = out
        self.parser = None
        self.resolver = None
        self.world = None

    def run(self):
        """Main game loop.
        
        User specifies actions for the player to take and the result of
        those actions is passed to out (default print).
        """
        # begin game
        # loop
        # get input
        # parse input
        # collect entities
        # take action
        # display the result
        # if player dead or quit goto end
        # goto loop
        # end
        # cleanup and say goodbye
        pass

    def _resolve_action(self, command):
        """Takes a parsed user command and executes it.

        Returns:
            str: A description of the results.
        """
        pass


class World:
    def __init__(self):
        self.name = "Untitled"
        self.welcome = "Welcome to my game!"
        self.opening = "You are in a very interesting place!"
        self.version = "0.0.0"
        self.player = None
        self.entities = {}
        self.events = {}
