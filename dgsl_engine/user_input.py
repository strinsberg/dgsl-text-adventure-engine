import enum
from . import actions
from . import commands


class ParseCodes(enum.Enum):
    BAD_VERB = 1
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
                code = ParseCodes.BAD_VERB
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

    def ask(self):
        for i, choice in enumerate(self.choices):
            self._out("{}. {}".format(str(i + 1), choice))
        self._out(str("{}. {}".format(len(self.choices + 1), "Cancel")))

        # Do some validation?
        return int(input("Choice: "))
