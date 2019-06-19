import enum


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
        noun = " ".join(words[1:])
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
            'subject': noun,
            'code': code,
            'message': message
        }


class Collector:
    """Visitor that collects all items that match with player input."""

    def __init__(self, parsed):
        self.parsed = parsed
        self.entities = []

    def visit_entity(self, entity):
        if entity.spec.name.find(self.parsed['subject']) > -1:
            self.entities.append(entity)

    def visit_container(self, container):
        self.visit_entity(container)
        for item in container:
            item.accept(self)


class Menu:
    pass
