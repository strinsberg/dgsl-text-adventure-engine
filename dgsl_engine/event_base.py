"""Base Event as well as supporting classes and functions."""
from . import actions


class Event:
    """Base for all Events that execute in response to player
    actions.

    Attributes:
        only_once (bool): True if the event should only be executed once.
        is_done (bool): If the event is finished and will not happen again.
        message (str): The message to return when the event executes.
        subjects (Event): Events to be notified when the event is executed.
            (Not implemented properly yet).
    """

    def __init__(self, obj_id):
        self.id = obj_id  # pylint: disable=invalid-name
        self.only_once = False
        self.is_done = False
        self.message = None
        self.subjects = []

    # Affected should just be the player
    def execute(self, affected):  # pylint: disable=unused-argument
        """Execute the event on the affected entity and return the
        result.

        Args:
          affected(Entity): The entity affected by the event.

        Returns:
          str: A description of the results.
        """
        if self.is_done:
            result = ''
        else:
            result = self.message if self.message is not None else ''
            self._check_if_done()
        # Add the results of subjects later
        return result

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_event(self)

    def register(self, event):
        """Register a given event as an observer."""
        self.subjects.append(event)

    def _check_if_done(self):
        if self.only_once:
            self.is_done = True

    def __repr__(self):
        return "<Event '{}'>".format(self.id)


# Should be move and be about the player
class MoveEntity(Event):
    """Event to move an entity to a destination.

    Currently only works for moving the player.

    Attributes:
        destination (Container): The Container to move the entity to.
    """

    def __init__(self, obj_id):
        super(MoveEntity, self).__init__(obj_id)
        self.destination = None

    def execute(self, affected):
        """Moves the Player(affected) to the destination."""
        actions.move(affected, self.destination)

        result = []

        super_result = super(MoveEntity, self).execute(affected)
        if super_result.strip() != '':
            result.append(super_result + '\n')

        # This definitely requires that this action is only for the player
        result.append(self.destination.enter(affected))

        return '\n'.join(result)

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_move(self)

    def __repr__(self):
        return "<Move '{}'>".format(self.id)


class Give(Event):
    """Transfers an item from a Container to the Player.

    Attributes:
        item_id (str): The id of the item to transfer.
        item_owner (str): The container to transfer the item from.
    """

    def __init__(self, obj_id):
        super(Give, self).__init__(obj_id)
        self.item_id = None
        self.item_owner = None

    def execute(self, affected):
        """Transfer the item from the item_owner to the Player(affected)."""
        item = self.item_owner.get(self.item_id)
        if item is not None:
            actions.move(item, affected)
        # Might want to add trigger for give events
        return super(Give, self).execute(affected)

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_give(self)

    def __repr__(self):
        return "<Give '{}'>".format(self.id)


class Take(Event):
    """Transfers a item from the player to a new container.

    Attributes:
        item_id (str): The item to transfer.
        new_owner (Container): The container to transfer the item to.
    """

    def __init__(self, obj_id):
        super(Take, self).__init__(obj_id)
        self.item_id = None
        self.new_owner = None

    def execute(self, affected):
        """Transfers the item from the player to the new owner."""
        item = affected.get(self.item_id)
        if item is not None:
            actions.move(item, self.new_owner)
        # Might want to add trigger for take events
        return super(Take, self).execute(affected)

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_take(self)

    def __repr__(self):
        return "<Take '{}'>".format(self.id)


class Toggle(Event):
    """Base class for events that toggle entity states.

    Attributes:
        target (Entity): The entity to toggle.
    """

    def __init__(self, obj_id):
        super(Toggle, self).__init__(obj_id)
        self.target = None

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_toggle(self)


class ToggleActive(Toggle):
    """Toggle the active state of an entity."""

    def execute(self, affected):
        """Toggles the state of the target."""
        if self.is_done:
            return ''
        self.target.states.toggle_active()
        return super(ToggleActive, self).execute(affected)

    def __repr__(self):
        return "<ToggleActive '{}'>".format(self.id)


class ToggleObtainable(Toggle):
    """Toggles weather an Entity is obtainable or not."""

    def execute(self, affected):
        """Toggles the obtainable state of the target."""
        if self.is_done:
            return ''
        self.target.states.toggle_obtainable()
        return super(ToggleObtainable, self).execute(affected)

    def __repr__(self):
        return "<ToggleObtainable '{}'>".format(self.id)


class ToggleHidden(Toggle):
    """Toggles the hidden state of an Entity."""

    def execute(self, affected):
        """Toggles the hidden state of the target."""
        if self.is_done:
            return ''
        if self.target is None:
            affected.states.toggle_hidden()
        else:
            self.target.states.toggle_hidden()
        return super(ToggleHidden, self).execute(affected)

    def __repr__(self):
        return "<ToggleHidden '{}'>".format(self.id)


class EndGame(Event):
    """Event to end the game."""

    def execute(self, affected):
        """Ends the game."""
        affected.states.hidden = True  # really only ever meant for the player
        return super(EndGame, self).execute(affected)

    def __repr__(self):
        return "<EndGame '{}'>".format(self.id)
