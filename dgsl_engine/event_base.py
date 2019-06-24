"""Base Event as well as supporting classes and functions."""
from abc import ABC, abstractmethod


class Event:
    """Base for all Events that execute in response to player
    actions."""

    def __init__(self, obj_id):
        self.id = obj_id
        self.only_once = False
        self.is_done = False
        self.subjects = []

    def execute(self, affected):
        """Execute the event on the affected entity and return the
        result.

        Args:
          affected(Entity): The entity affected by the event.

        Returns:
          str: A description of the results.

        """
        # All the base version does is notify it's observers
        # You have to subclass or decorate it
        return ""

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


class EventDecorator(Event, ABC):
    """Abstract class for event decorators."""

    def __init__(self, event):  # pragma: no cover
        Event.__init__(self, event.id)
        self.event = event
        self.id = event.id
        ABC.__init__(self)  # is this the right order?

    @abstractmethod
    def execute(self, affected):  # pragma: no cover
        """

        Args:
          affected:

        Returns:

        """

    @abstractmethod
    def accept(self, visitor):  # pragma: no cover
        """

        Args:
          visitor:

        Returns:

        """
