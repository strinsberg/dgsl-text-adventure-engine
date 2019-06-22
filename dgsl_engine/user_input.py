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


class ActionResolver:
    def __init__(self, entity_collector):
        self.collector = entity_collector

    def resolve_input(self, parsed_input, world):
        if parsed_input['code'] is not None:
            return parsed_input['message']

        entities = self.collector.collect(parsed_input['object'],
                                          parsed_input['other'],
                                          world.player.owner)
        size = len(entities)
        if size > 1:
            menu = Menu(entities)
            idx = menu.ask()
            if idx != size:
                entity = entities[idx]
            else:
                return "Cancelled"

        if size == 1:
            entity = entities[0]
        elif size == 0:
            pass

        # Eventually add the other collecting code
        return actions.take_action(parsed_input['verb'], entity, None, world)


class Collector:
    """Visitor that collects all items that match with player input."""

    def __init__(self):
        self.obj = None
        self.other = None
        self.entities = []

    def collect(self, obj, other, entity):
        self.obj = obj
        self.other = other
        entity.accept(self)
        return self.entities

    def visit_entity(self, entity):
        if entity.spec.name.find(self.obj) > -1:
            self.entities.append(entity)

    def visit_container(self, container):
        self.visit_entity(container)
        for item in container:
            item.accept(self)


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
