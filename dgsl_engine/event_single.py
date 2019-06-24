"""Single events."""
from . import event_base
from . import actions


class MoveEntity(event_base.Event):
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
