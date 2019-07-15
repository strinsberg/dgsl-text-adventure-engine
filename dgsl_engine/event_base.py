"""Base Event as well as supporting classes and functions."""
from . import actions


class Event:
    """Base for all Events that execute in response to player
    actions."""

    def __init__(self, obj_id):
        self.id = obj_id
        self.only_once = False
        self.is_done = False
        self.message = None
        self.subjects = []

    # Affected should just be the player
    def execute(self, affected):
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
            if self.only_once:
                self.is_done = True
        # Add the results of observers later
        return result

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_event(self)

    def register(self, event):
        """

        Args:
          event:

        Returns:

        """
        self.subjects.append(event)

    def __repr__(self):
        return "<Event '{}'>".format(self.id)


# Should be move and be about the player
class MoveEntity(Event):
    """Event to move an entity to a destination."""

    def __init__(self, obj_id):
        super(MoveEntity, self).__init__(obj_id)
        self.destination = None

    def execute(self, affected):
        """

        Args:
          affected:

        Returns:

        """
        actions.move(affected, self.destination)
        return super(MoveEntity, self).execute(affected)

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_move(self)

    def __repr__(self):
        return "<Move '{}'>".format(self.id)


class Give(Event):
    def __init__(self, obj_id):
        super(Give, self).__init__(obj_id)
        self.item_id = None
        self.item_owner = None

    def execute(self, affected):
        item = self.item_owner.get(self.item_id)
        if item is not None:
            actions.move(item, affected)
        return super(Give, self).execute(affected)

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_give(self)

    def __repr__(self):
        return "<Give '{}'>".format(self.id)


class Take(Event):
    def __init__(self, obj_id):
        super(Take, self).__init__(obj_id)
        self.item_id = None
        self.new_owner = None

    def execute(self, affected):
        item = affected.get(self.item_id)
        if item is not None:
            actions.move(item, self.new_owner)
        return super(Take, self).execute(affected)

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_take(self)

    def __repr__(self):
        return "<Take '{}'>".format(self.id)


class Toggle(Event):
    def __init__(self, obj_id):
        super(Toggle, self).__init__(obj_id)
        self.target = None

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_toggle(self)


class ToggleActive(Toggle):
    def execute(self, affected):
        if self.is_done:
            return ''
        self.target.states.toggle_active()
        return super(ToggleActive, self).execute(affected)

    def __repr__(self):
        return "<ToggleActive '{}'>".format(self.id)


class ToggleObtainable(Toggle):
    def execute(self, affected):
        if self.is_done:
            return ''
        self.target.states.toggle_obtainable()
        return super(ToggleObtainable, self).execute(affected)

    def __repr__(self):
        return "<ToggleObtainable '{}'>".format(self.id)


class ToggleHidden(Toggle):
    def execute(self, affected):
        if self.is_done:
            return ''
        if self.target is None:
            affected.states.toggle_hidden()
        else:
            self.target.states.toggle_hidden()
        return super(ToggleHidden, self).execute(affected)

    def __repr__(self):
        return "<ToggleHidden '{}'>".format(self.id)
