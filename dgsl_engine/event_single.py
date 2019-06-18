from . import event_base
from . import actions


class MoveEntity(event_base.Event):
    def __init__(self, obj_id):
        super(MoveEntity, self).__init__(obj_id)
        self.destination = None

    def execute(self, affected):
        actions.move(affected, self.destination)
        return super(MoveEntity, self).execute(affected)