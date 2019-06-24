"""Classes and functions for getting and processing user input."""
import enum
from . import commands


class ParseCodes(enum.Enum):
    """Enum for parser return codes."""
    ERROR = 1
    COMMAND = 2


class Parser:
    """Turns raw user input into form useable by a resolver."""

    def __init__(self):
        self.verbs = ['get', 'take', 'drop', 'use', 'look', 'inventory']
        self.commands = ['quit', 'exit']

    def parse(self, user_input):
        """

        Args:
          user_input:

        Returns:

        """
        words = user_input.strip().split()
        verb = words[0]
        obj = " ".join(words[1:])
        other = None
        code = None
        message = None

        if verb not in self.verbs:
            if verb in self.commands:
                code = ParseCodes.COMMAND
            else:
                code = ParseCodes.ERROR
                message = "You don't know how to " + verb

        return {
            'verb': verb,
            'object': obj,
            'other': other,
            'code': code,
            'message': message
        }


class Menu:
    """Asks a user to choose one of a list of choices."""

    def __init__(self, choices, out=print):
        self.choices = choices
        self._out = out

    def ask(self, input_=None):
        """

        Args:
          input_:  (Default value = None)

        Returns:

        """
        for i, choice in enumerate(self.choices):
            self._out("{}. {}\n".format(str(i + 1), choice))
        self._out(str("{}. {}\n".format(len(self.choices) + 1, "Cancel")))

        # Do some validation?
        if input_ is None:
            # Can replace all of this if I can figure out how to send input
            # like with streams in c++. And remove the no cover.
            result = int(input("Choice: "))  # pragma: no cover
        else:
            result = int(input_[0])

        if result > len(self.choices) + 1:
            return -1
        return result


class MenuFactory:
    """Creates a Menu"""

    def make(self, choices):
        """

        Args:
          choices:

        Returns:

        """
        return Menu(choices)
