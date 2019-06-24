"""Decorators for wrapping single events in."""
from . import event_base


class MessageDecorator(event_base.EventDecorator):
    """Decorator to add a message to an event.

    Attributes:
        event (Event): The event to decorate.
        message (str): The message to add.
    """

    def __init__(self, event, message):
        super(MessageDecorator, self).__init__(event)
        self.message = message

    def execute(self, affected):
        """Execute the event on affected entity.

        Args:
            affected (Entity): The entity affected by the event.

        Returns:
            str: The results of the execution.
        """
        result = self.event.execute(affected)
        if result != "":
            self.message = result + '\n' + self.message
        return self.message

    def accept(self, visitor):
        """Accepts a visitor.

        Args:
            visitor (Visitor): The visitor to accept.
        """
        # Probably should do something for the decorator too at some point?
        self.event.accept(visitor)
