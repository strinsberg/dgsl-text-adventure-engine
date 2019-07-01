"""Classes and supporting functions for resolving and executing
actions."""
from abc import ABC, abstractmethod


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
    """Factory to return action objects."""

    def new(self, verb, player, entity, other):
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
        if verb in ['talk']:
            return Talk(player, entity, other)
        return NullAction(player, entity, other)


class Action(ABC):
    """An action taken by the player.

    Attributes:
        player (Player): The player character taking the action.
        entity (Entity): The entity that was the direct object of
            the verb.
        other (Entity): The entity that was the indirect object of
            the verb.
    """

    def __init__(self, player, entity, other):
        self.player = player
        self.entity = entity
        self.other = other
        super(Action, self).__init__()

    @abstractmethod
    def take_action(self):  # pragma: no cover
        """Executes the action.

        Returns:
            str: The results of the actions execution.
        """

    def _execute_event(self, verb):
        if self.entity.events.has_event(verb):
            return self.entity.events.execute(verb, self.player)
        return None


class NullAction(Action):
    """Null action that says nothing happend."""

    def take_action(self):
        """See Action."""
        return "Nothing happens"


class Get(Action):
    """Action to get an object from the players room."""

    def take_action(self):
        """See Action."""
        if self.entity is None:
            return "Get what?"
        if self.player.inventory.has_item(self.entity.spec.id):
            return "You already have it"
        if self.entity.states.obtainable:
            move(self.entity, self.player)
            moved = "You take " + self.entity.spec.name
            result = self._execute_event('get')
            if result is not None:
                return "{}\n{}".format(moved, result)
            return moved
        return "You can't take that"


class Drop(Action):
    """Action to drop an object the player is carrying."""

    def take_action(self):
        """See Action."""
        if self.entity is None:
            return "Drop what?"
        if self.player.inventory.has_item(self.entity.spec.id):
            move(self.entity, self.player.owner)
            dropped = "You drop " + self.entity.spec.name
            result = self._execute_event('drop')
            if result is not None:
                return "{}\n{}".format(dropped, result)
            return dropped
        return "You don't have it"


class Use(Action):
    """An action to use an object."""

    def take_action(self):
        """See Action."""
        if self.entity is None:
            return "Use what?"
        if self.entity.events.has_event('use'):
            result = self.entity.events.execute('use', self.player)
            used = "You use " + self.entity.spec.name
            return "{}\n{}".format(used, result)
        return "You can't use that"


class Look(Action):
    """An action to look at an object."""

    def take_action(self):
        """See Action."""
        if self.entity is not None:
            description = "You see " + self.entity.describe()
            result = self._execute_event('look')
            if result is not None:
                return "{}\n{}".format(description, result)
            return description
        return self.player.owner.describe()


class CheckInventory(Action):
    """Action to list the contents of the players inventory or check to
    see if an object is in it."""

    def take_action(self):
        """See Action."""
        if self.entity is None:
            result = ["You are carrying ..."]
            if self.player.inventory.items:
                for item in self.player:
                    result.append(item.describe())
            else:
                result.append("Nothing")
            return "\n".join(result)

        if self.player.inventory.has_item(self.entity.spec.id):
            return "You have that"
        return "You don't have that"


class Talk(Action):
    def take_action(self):
        if self.entity is not None:
            result = self._execute_event('talk')
            if result is not None:
                return result
            return "That doesn't talk"
        return "To whom?"


def move(entity, destination):
    """Moves an entity to a new container.

    Args:
        entity (Entity): The entity to move.
        destination (Container): The container to move the entity into.
    """
    here = entity.owner
    if destination.add(entity):
        here.inventory.remove(entity.spec.id)
