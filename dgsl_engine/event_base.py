"""
Base Event as well as supporting classes and functions.
"""
from abc import ABC, abstractmethod


class Event(ABC):
    """ABC for all Events that execute in response to player actions.
    
    Attributes:
      id (str): A unique identifier.
      only_once (bool): If the event should only be executed once.
      is_done (bool): If the event is finished and won't run again.
    """

    def __init__(self, obj_id):
        self.id = obj_id
        self.only_once = False
        self.is_done = False
        super(Event, self).__init__()

    @abstractmethod
    def execute(self, affected):
        """Execute the event on the affected entity and return the result.

        Args:
          affected (Entity): The entity affected by the event.

        Returns:
          str: A description of the results.
        """
        pass