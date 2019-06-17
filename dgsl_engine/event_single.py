from . import event_base


class MoveEntity(event_base.Event):
    def __init__(self, obj_id):
        super(MoveEntity, self).__init__(obj_id)
        self.destination = None

    def execute(self, affected):
        # here = affected.owner
        # here.inventory.remove(affected.spec.id)
        # self.destination.inventory.add(affected)
        pass