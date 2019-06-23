import enum
from . import actions
from . import commands


class ParseCodes(enum.Enum):
    ERROR = 1
    COMMAND = 2


class Parser:
    def __init__(self):
        self.verbs = ['get', 'use']
        self.commands = ['quit', 'exit']

    def parse(self, user_input):
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
    def __init__(self, choices, out=print):
        self.choices = choices
        self._out = out

    def ask(self, input_=None):
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
    def make(self, choices):
        return Menu(choices)