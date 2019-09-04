"""Classes and functions for getting and processing user input."""
import enum


class ParseCodes(enum.Enum):
    """Enum for parser return codes."""
    ERROR = 1
    COMMAND = 2


class Parser:  # pylint: disable=too-few-public-methods
    """Turns raw user input into form useable by a resolver.

    Attributes:
        verbs: A list of acceptable verbs.
        commands: A list of commands.
    """

    def __init__(self):
        self.verbs = ['get', 'take', 'drop', 'equip', 'remove', 'go',
                      'use', 'look', 'inventory', 'talk', 'give', 'put']
        self.commands = ['quit', 'exit']

    def parse(self, user_input):
        """Parses a string of user input.

        Args:
          user_input (str): The user input to parse.

        Returns:
            dict: A dictionary with the split up parts of the input.
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


class Menu:  # pylint: disable=too-few-public-methods
    """Asks a user to choose one of a list of choices.

    Attributes:
        choices: A list of menu items to choose from.
    """

    def __init__(self, choices, out=print, _in=input):
        self.choices = choices
        self._out = out
        self._in = _in

    def ask(self, input_=None):
        """Display the menu choices and asks for a choice.

        Args:
          input_: input to use (only for testing, should be eliminated).

        Returns:
            int: The chosen menu item.
        """
        for i, choice in enumerate(self.choices):
            self._out("{}. {}".format(str(i + 1), choice))
        self._out(str("{}. {}".format(len(self.choices) + 1, "Cancel")))
        self._out()

        # Validate to make sure it is an int?
        if input_ is None:
            try:
                result = int(self._in("Choice: "))
            except ValueError:
                return -1
        else:
            result = int(input_[0])

        if result > len(self.choices) + 1:
            return -1
        return result - 1  # Because the menu item is i + 1


class MenuFactory:  # pylint: disable=too-few-public-methods
    """Creates a Menu"""

    def make(self, choices):  # pylint: disable=no-self-use
        """Returns a menu with the choices."""
        return Menu(choices)
