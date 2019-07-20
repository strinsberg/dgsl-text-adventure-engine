"""Classes and supporting functions for resolving and executing
actions."""
from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods
# They must be objects for polymorphism and only need one method


class ActionResolver:
    """Takes parsed user input and executes the desired action.

    This can include letting the user know they made a mistake.

    Attributes:
        collector_fact (EntityCollectorFactory): A factory to create
            the desired type of EntityCollector to collect objects based
            on the parsed input.
        menu_factory (MenuFactory): A factory to create the desired menu
            to ask the user to make a choice when their input could
            match more than one entity.
        action_factory (ActionFactory): A factory to create action
            objects for valid parsed actions.
    """

    def __init__(self, collector_factory, menu_factory, action_factory):
        self.collector_fact = collector_factory
        self.menu_factory = menu_factory
        self.action_factory = action_factory

    def resolve_input(self, parsed_input, player):
        """Resolves a parsed input and returns the result.

        Args:
            parsed_input (dict): A dict with text split up by the
                parser. (see user_input.Parser)
            player (Player): The player character taking the actions.

        Returns:
            str: The result of the actions resolution.
        """
        message = None

        action = self.action_factory.new(parsed_input['verb'], player)

        if not parsed_input['object'].strip():
            entity = None
            other = None
        else:
            entity, other, message = self._get_entities(
                parsed_input, player, action)
            if message != '\n' and message is not None:
                return message

        result = action.take_action(entity, other)
        if result != '' and message == '\n':
            result = message + result
        return result

    def _get_entities(self, parsed_input, player, act):
        collector = self.collector_fact.make(parsed_input['object'],
                                             parsed_input['other'],
                                             player.owner)

        entities = act.filter_entities(collector.collect())

        entity = None
        other = None
        message = None

        size = len(entities)
        if size > 1:
            choices = [entity.spec.name for entity in entities]
            menu = self.menu_factory.make(choices)
            idx = menu.ask()

            message = '\n'
            if idx == -1:
                message += "That is not a choice"
            elif idx == size:
                message += 'Cancelled'
            else:
                entity = entities[idx]

        elif size == 1:
            entity = entities[0]
        else:
            message = "There is no " + parsed_input['object']

        return entity, other, message


class ActionFactory:
    """Factory to return action objects."""

    def new(self, verb, player):  # pylint: disable=no-self-use
        """Creates a new action object based on the given verb.

        Args:
            verb (str): The verb of the action.
            player (Player): The player character taking the action.
            entity (Entity): The entity that was the direct object of
                the verb.
            other (Entity): The entity that was the indirect object of
                the verb.

        Returns:
            Action: The new action. If the verb does not exist returns
                a null action.
        """
        action = NullAction(player)
        if verb in ['get', 'take']:
            action = Get(player)
        elif verb in ['use']:
            action = Use(player)
        elif verb in ['drop']:
            action = Drop(player)
        elif verb in ['look']:
            action = Look(player)
        elif verb in ['inventory']:
            action = CheckInventory(player)
        elif verb in ['talk']:
            action = Talk(player)
        elif verb in ['equip']:
            action = Equip(player)
        elif verb in ['remove']:
            action = Remove(player)
        elif verb in ['go']:
            action = Go(player)
        elif verb in ['give', 'put']:
            action = Place(player)
        return action


class Action(ABC):
    """An action taken by the player.

    Attributes:
        player (Player): The player character taking the action.
    """

    def __init__(self, player):
        self.player = player
        super(Action, self).__init__()

    @abstractmethod
    def take_action(self, entity, other):  # pragma: no cover
        """Executes the action.

        Args:
            entity (Entity): The entity that was the direct object of
                the verb.
            other (Entity): The entity that was the indirect object of
                the verb.

        Returns:
            str: The results of the actions execution.
        """

    def _execute_event(self, verb, entity):
        if entity.events.has_event(verb):
            return entity.events.execute(verb, self.player)
        return None

    def filter_entities(self, entities):
        return entities


class NullAction(Action):
    """Null action that says nothing happend."""

    def take_action(self, entity, other):
        """See Action."""
        return "Nothing happens"


class Get(Action):
    """Action to get an object from the players room."""

    def take_action(self, entity, other):
        """See Action."""
        if entity is None:
            return "Get What?"
        if self.player.inventory.has_item(entity.spec.id):
            return "You already have it!"
        if entity.states.obtainable:
            move(entity, self.player)
            moved = "You take " + entity.spec.name
            result = self._execute_event('get', entity)
            if result is not None:
                return "{}\n{}".format(moved, result)
            return moved
        return "You can't take that"

    def filter_entities(self, entities):
        if len(entities) <= 1:
            return entities
        result = []
        for item in entities:
            entity = self.player.get(item.spec.id)
            if entity is None and item is not self.player:
                result.append(item)
        return result


class Drop(Action):
    """Action to drop an object the player is carrying."""

    def take_action(self, entity, other):
        """See Action."""
        if entity is None:
            return "Drop What?"
        if self.player.inventory.has_item(entity.spec.id):
            move(entity, self.player.owner)
            dropped = "You drop " + entity.spec.name
            result = self._execute_event('drop', entity)
            if result is not None:
                return "{}\n{}".format(dropped, result)
            return dropped
        return "You don't have that"


class Use(Action):
    """An action to use an object."""

    def take_action(self, entity, other):
        """See Action."""
        if entity is None:
            return "Use What?"
        if not entity.states.active:
            # replace with an inactive message eventually
            return "For some reason you can't"
        if entity.events.has_event('use'):
            result = entity.events.execute('use', self.player)
            if result.strip() == '':
                return "You use " + entity.spec.name
            return result
        return "You can't use that"


class Look(Action):
    """An action to look at an object."""

    def take_action(self, entity, other):
        """See Action."""
        if entity is not None:
            description = "You see " + entity.describe()
            result = self._execute_event('look', entity)
            if result is not None:
                return "{}\n{}".format(description, result)
            return description
        return self.player.owner.describe()


class CheckInventory(Action):
    """Action to list the contents of the players inventory or check to
    see if an object is in it."""

    def take_action(self, entity, other):
        """See Action."""
        if entity is None:
            result = ["You are carrying ..."]
            if self.player.inventory.items:
                for item in self.player:
                    result.append(item.spec.name)
            else:
                result.append("Nothing")

            result.append("\nYou are wearing ...")
            if self.player.equipped.equipment:
                for item in self.player.equipped:
                    result.append(item.spec.name)
            else:
                result.append("Nothing")

            return "\n".join(result)

        if self.player.inventory.has_item(entity.spec.id):
            return "You have that"
        return "You don't have that"


class Talk(Action):
    """empty"""

    def take_action(self, entity, other):
        if entity is not None:
            if not entity.states.active:
                # perhaps replace with an inactive message
                return "They don't have anything to say right now."
            result = self._execute_event('talk', entity)
            if result is not None:
                return result
            return "That doesn't talk"
        return "To whom?"


class Equip(Action):
    def take_action(self, entity, other):
        if entity is None:
            return "Equip what?"
        # To properly deal with conditional events related to equipping
        # things the actual equip would need to be an event. Then if there
        # is an event (of the right type) it could be consulted. If there is
        # not then the equipment could just be equipped.
        try:
            old_owner = entity.owner
            self.player.equipped.equip(entity)
            old_owner.inventory.remove(entity.spec.id)
            message = 'You equip it'
            if entity.events.has_event('equip'):
                result = entity.events.execute('equip', self.player)
                if result != '':
                    return message + '\n' + result
            return message
        except AttributeError:
            return "You can't equip that!"


class Remove(Action):
    def take_action(self, entity, other):
        if entity is None:
            return "Remove What?"
        slot = self.player.equipped.wearing(entity)
        if slot is not None:
            equipment = self.player.equipped.remove(slot)
            self.player.add(equipment)
            message = "You remove it"
            if entity.events.has_event('remove'):
                result = entity.events.execute('remove', self.player)
                if result != '':
                    return message + '\n' + result
            return message
        return "You are not wearing that!"


# Will most likely need multi verb events for this to work with use
class Go(Action):
    def take_action(self, entity, other):
        if entity is None:
            return "Go Where?"
        if not entity.states.active:
            return "For some reason you can't"
        if entity.events.has_event('go'):
            return entity.events.execute('go', self.player)
        return "Impossible!"


class Place(Action):
    def take_action(self, entity, other):
        return "Sorry, that action is not yet available."


def move(entity, destination):
    """Moves an entity to a new container.

    Args:
        entity (Entity): The entity to move.
        destination (Container): The container to move the entity into.
    """
    here = entity.owner
    if destination.add(entity):
        here.inventory.remove(entity.spec.id)
