"""
Classes of Entities that can contain other entities and related
functions and exceptions.
"""
from functools import singledispatch
from . import entity_base
from . import collectors


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
        """empty"""
        collector = collectors.EntityIdCollector(item_id, self)
        return collector.collect()

    def describe(self):
        desc = [self.spec.description]
        if self.states.active:
            desc.extend(
                ["It holds " + item.spec.name for item in self.inventory])
        return "\n".join(desc)

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

    def describe(self):
        desc = [self.spec.description]
        desc.extend(
            ["There is " + item.spec.name for item in self.inventory
             if not isinstance(item, Player)])
        return "\n".join(desc)

    def enter(self, affected):
        result = []
        result.append(self.describe())
        if self.events.has_event('enter'):
            enter = self.events.execute('enter', affected)
            if enter != '':
                result.append('')
                result.append(enter)
        return '\n'.join(result)

    def accept(self, visitor):
        visitor.visit_room(self)

    def __repr__(self):
        return "<Room '{}', Name: '{}', Contents: {}>".format(
            self.spec.id, self.spec.name, self._repr_contents())


# Should be an ABC
class Character(Container):
    """empty"""

    def __init__(self, obj_id):
        super(Character, self).__init__(obj_id)
        self.equipped = entity_base.Equipped(self)

    def describe(self):
        return self.spec.description


class Player(Character):
    """The player character.

    Cannot contain Rooms.
    """

    def __init__(self, obj_id):
        super(Player, self).__init__(obj_id)
        self.states.active = True
        self.states.obtainable = False
        self.states.hidden = False

    def accept(self, visitor):
        visitor.visit_player(self)

    def __repr__(self):
        return "<Player '{}', Name: '{}', Contents: {}>".format(
            self.spec.id, self.spec.name, self._repr_contents())


class Npc(Character):
    """A non player character.

    Items it holds cannot be found when looking for items.
    """

    def __repr__(self):
        return "<Npc '{}', Name: '{}', Contents: {}>".format(
            self.spec.id, self.spec.name, self._repr_contents())

    def accept(self, visitor):
        visitor.visit_npc(self)


# Exceptions ###########################################################

class ContainerError(Exception):
    """Exception for adding the wrong item type to a container."""


# Helpers ##############################################################

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
