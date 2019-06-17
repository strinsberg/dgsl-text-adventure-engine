from . import event_base


class MoveEntity(event_base.Event):
    def __init__(self, obj_id):
        super(MoveEntity, self).__init__(obj_id)
        self.destination = None

    def execute(self, affected):
        here = affected.owner
        if self.destination.add(affected):
            here.inventory.remove(affected.spec.id)
        return super(MoveEntity, self).execute(affected)