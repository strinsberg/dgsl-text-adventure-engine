from . import entity_base


class Container(entity_base.Entity):
    """Entity that can have other entities inside of it.
    
    Cannot hold a Player.

    Attributes:
        inventory (Inventory): The inventory that holds the entities.
    """

    def __init__(self, obj_id):
        entity_base.Entity.__init__(self, obj_id)
        self.inventory = entity_base.Inventory()


class Room(Container):
    """A location in a World that can hold players."""

    def __init__(self, obj_id):
        Container.__init__(self, obj_id)


class Player(Container):
    """The player character."""

    def __init__(self, obj_id):
        Container.__init__(self, obj_id)
