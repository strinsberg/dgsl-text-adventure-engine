"""
Base Event as well as supporting classes and functions.
"""
from abc import ABC, abstractmethod


class Event:
    """Base for all Events that execute in response to player actions.
    
    Attributes:
      id (str): A unique identifier.
      only_once (bool): If the event should only be executed once.
      is_done (bool): If the event is finished and won't run again.
    """

    def __init__(self, obj_id):
        self.id = obj_id
        self.only_once = False
        self.is_done = False

    def execute(self, affected):
        """Execute the event on the affected entity and return the result.

        Args:
          affected (Entity): The entity affected by the event.

        Returns:
          str: A description of the results.
        """
        # All the base version does is notify it's observers
        # You have to subclass or decorate it
        return ""

    def accept(self, visitor):
        visitor.visit_event(self)


class EventDecorator(Event, ABC):
    def __init__(self, event):  # pragma: no cover
        Event.__init__(self, event.id)
        self.event = event
        self.id = event.id
        ABC.__init__(self)  # is this the right order?

    @abstractmethod
    def execute(self, affected):  # pragma: no cover
        pass

    @abstractmethod
    def accept(self, visitor):  # pragma: no cover
        pass