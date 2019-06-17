"""
Classes of Entities that can contain other entities and related
functions and exceptions.
"""
from functools import singledispatch
from . import entity_base


class Container(entity_base.Entity):
    """Entity that can have other entities inside of it.
    
    Cannot hold a Player or a Room.

    Attributes:
        inventory (Inventory): The inventory that holds the entities.
    """

    def __init__(self, obj_id):
        entity_base.Entity.__init__(self, obj_id)
        self.inventory = entity_base.Inventory()

    def add(self, item):
        """Add an item to the container.
        
        Returns:
            bool: True if the item is added to the containers inventory.
        
        Raises:
            ContainerError: If the item is a Player or a Room.
        """
        return _add_to_container(item, self)


class Room(Container):
    """A location in a World that can hold players."""

    def __init__(self, obj_id):
        Container.__init__(self, obj_id)

    def add(self, item):
        """See Container.add.

        Raises:
            ContainerError: If  the entity is a Room.
        """
        return _add_to_room(item, self)


class Player(Container):
    """The player character."""

    def __init__(self, obj_id):
        Container.__init__(self, obj_id)


class ContainerError(Exception):
    """Exception for adding the wrong item type to a container."""
    pass


@singledispatch
def _add_to_container(item, container):
    return container.inventory.add(item)


@_add_to_container.register(Room)
@_add_to_container.register(Player)
def _(item, container):
    raise ContainerError("Error: Can't add " + str(type(item)) + " to a " +
                         str(type(container)))


@singledispatch
def _add_to_room(item, room):
    return room.inventory.add(item)


@_add_to_room.register(Room)
def _(item, room):
    raise ContainerError("Error: Can't add a Room to a Room")
