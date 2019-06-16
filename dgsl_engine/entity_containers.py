from . import entity_base


class Container(entity_base.Entity):
    def __init__(self, obj_id):
        entity_base.Entity.__init__(self, obj_id)
        self.inventory = entity_base.Inventory()


class Room(Container):
    def __init__(self, obj_id):
        Container.__init__(self, obj_id)


class Player(Container):
    def __init__(self, obj_id):
        Container.__init__(self, obj_id)
