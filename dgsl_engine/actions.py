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

        action = self.action_factory.new(parsed_input['verb'], player, entity,
                                         other)
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

            if idx == -1:
                message = "That is not a choice"
            elif idx == size:
                message = 'Cancelled'
            else:
                entity = entities[idx]

        elif size == 1:
            entity = entities[0]
        else:
            message = "There is no " + parsed_input['object']

        return entity, other, message


class ActionFactory:
    def new(self, verb, player, entity, other):
        if verb in ['get', 'take']:
            return Get(player, entity, other)
        if verb in ['use']:
            return Use(player, entity, other)
        if verb in ['drop']:
            return Drop(player, entity, other)
        if verb in ['look']:
            return Look(player, entity, other)
        if verb in ['inventory']:
            return CheckInventory(player, entity, other)
        return NullAction(player, entity, other)


class Action(ABC):
    def __init__(self, player, entity, other):
        self.player = player
        self.entity = entity
        self.other = other
        super(Action, self).__init__()

    @abstractmethod
    def take_action(self):  # pragma: no cover
        pass

    def _execute_event(self, verb):
        if self.entity.events.has_event(verb):
            return self.entity.events.execute(verb, self.player)
        return ''

    def _add_result(self, text, result):
        if result.strip() == '':
            return text
        return "{}\n{}".format(text, result)


class NullAction(Action):
    def take_action(self):
        return "Nothing happens"


class Get(Action):
    def take_action(self):
        if self.entity is None:
            return "Get what?"
        if self.player.inventory.has_item(self.entity.spec.id):
            return "You already have it"
        if self.entity.states.obtainable:
            move(self.entity, self.player)
            moved = "You take " + self.entity.spec.name
            result = self._execute_event('get')
            return self._add_result(moved, result)
        return "You can't take that"


class Drop(Action):
    def take_action(self):
        if self.entity is None:
            return "Drop what?"
        if self.player.inventory.has_item(self.entity.spec.id):
            move(self.entity, self.player.owner)
            dropped = "You drop " + self.entity.spec.name
            result = self._execute_event('drop')
            return self._add_result(dropped, result)
        return "You don't have it"


class Use(Action):
    def take_action(self):
        if self.entity is None:
            return "Use what?"
        if self.entity.events.has_event('use'):
            result = self.entity.events.execute('use', self.player)
            used = "You use " + self.entity.spec.name
            return self._add_result(used, result)
        return "You can't use that"


class Look(Action):
    def take_action(self):
        if self.entity is not None:
            description = "You see " + self.entity.describe()
            result = self._execute_event('look')
            return self._add_result(description, result)
        return self.player.owner.describe()


class CheckInventory(Action):
    def take_action(self):
        if self.entity is None:
            result = ["You are carrying ..."]
            if self.player.inventory.items:
                for item in self.player:
                    result.append(item.describe())
            else:
                result.append("Nothing")
            return "\n".join(result)
        else:
            if self.player.inventory.has_item(self.entity.spec.id):
                return "You have that"
            return "You don't have that"


def move(entity, destination):
    here = entity.owner
    if destination.add(entity):
        here.inventory.remove(entity.spec.id)
