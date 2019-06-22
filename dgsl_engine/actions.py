from abc import ABC, abstractmethod
from . import user_input


class ActionResolver:
    def __init__(self, collector_factory, menu_factory, action_factory):
        self.collector_fact = collector_factory
        self.menu_factory = menu_factory
        self.action_factory = action_factory

    def resolve_input(self, parsed_input, player):
        if not parsed_input['object'].strip():
            entity = None
            other = None
        else:
            entity, other, message = self._get_entities(parsed_input, player)
            if message is not None:
                return message

        action = self.action_factory(parsed_input['verb'], entity, other,
                                     player)
        return action.take_action()

    def _get_entities(self, parsed_input, player):
        collector = self.collector_fact.make(parsed_input['object'],
                                             parsed_input['other'],
                                             player.owner)
        entities = collector.collect()

        entity = None
        other = None
        message = None

        size = len(entities)
        if size > 1:
            menu = self.menu_factory.make(entities)
            idx = menu.ask()

            if idx != size:
                entity = entities[idx]
            else:
                message = "Cancelled"

        if size == 1:
            entity = entities[0]
        elif size == 0:
            message = "There is no " + parsed_input['object']

        return entity, other, message


class ActionFactory:
    def new(self, verb, player, entity, other):
        if verb in ['get', 'take']:
            return Get(player, entity, other)
        if verb in ['use']:
            return Use(player, entity, other)
        else:
            return NullAction(player, entity, other)


class Action(ABC):
    def __init__(self, player, entity, other):
        self.player = player
        self.entity = entity
        self.other = other
        super(Action, self).__init__()

    @abstractmethod
    def take_action(self):
        pass


class NullAction(Action):
    def take_action(self):
        return "Nothing Happens"


class Get(Action):
    def take_action(self):
        if self.entity.states.obtainable:
            move(self.entity, self.player)
            return "You take " + self.entity.spec.name
        return "You can't take that"


class Use(Action):
    def take_action(self):
        if self.entity.events.has_event('use'):
            return "You use " + self.entity.spec.name
        return "You can't use that"


################################################333


def _take_action(verb, entity, other, world):
    # will eventually have to deal with other. Might just pass it to the action.
    if verb == 'get':
        message = _get(world.player, entity)
    elif verb == 'use':
        message = _use(world.player, entity)
    else:
        # For testing action resolver. Should never be called otherwise as a
        # bad verb will result in a parse error.
        message = 'Nothing to say'

    if entity.events.has_event(verb):
        print(entity.events.execute(verb, entity))
        message += "\n" + entity.events.execute(verb, entity)
    return message


def move(entity, destination):
    here = entity.owner
    if destination.add(entity):
        here.inventory.remove(entity.spec.id)


def _get(player, entity):
    if entity.states.obtainable:
        move(entity, player)
        return "You take " + entity.spec.name
    return "You can't take that"


def _use(player, entity):
    if entity.events.has_event('use'):
        return "You use " + entity.spec.name
    return "You can't use that"