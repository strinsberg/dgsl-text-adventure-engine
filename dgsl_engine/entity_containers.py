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

    def __iter__(self):
        return self.inventory.__iter__()

    def add(self, item):
        """Add an item to the container.

        Returns:
            bool: True if the item is added to the containers inventory.

        Raises:
            ContainerError: If the item is a Player or a Room.
        """
        if _add_to_container(item, self):
            item.owner = self
            return True
        return False

    def get(self, item_id):
        if self.inventory.has_item(item_id):
            return self.inventory.items[item_id]
        return None

    def accept(self, visitor):
        visitor.visit_container(self)

    def __repr__(self):
        return "<Container '{}', Name: '{}', Contents: {}>".format(
            self.spec.id, self.spec.name, self._repr_contents())

    def _repr_contents(self):
        contents = []
        for item in self:
            contents.append(repr(item))
        return '{' + ", ".join(contents) + '}'


class Room(Container):
    """A location in a World that can hold any entity except other rooms."""

    def __init__(self, obj_id):
        Container.__init__(self, obj_id)
        self.states.active = True
        self.states.obtainable = False
        self.states.hidden = False

    def add(self, item):
        """See Container.add.

        Raises:
            ContainerError: If  the entity is a Room.
        """
        if _add_to_room(item, self):
            item.owner = self
            return True
        return False

    def __repr__(self):
        return "<Room '{}', Name: '{}', Contents: {}>".format(
            self.spec.id, self.spec.name, self._repr_contents())


class Player(Container):
    """The player character.

    Cannot contain Rooms.
    """

    def __init__(self, obj_id):
        Container.__init__(self, obj_id)
        self.states.active = True
        self.states.obtainable = False
        self.states.hidden = False

    def __repr__(self):
        return "<Player '{}', Name: '{}', Contents: {}>".format(
            self.spec.id, self.spec.name, self._repr_contents())


class ContainerError(Exception):
    """Exception for adding the wrong item type to a container."""


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
