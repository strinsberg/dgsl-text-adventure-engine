"""empty"""


class EntityCollector:
    """Visitor that collects all items that match with player input.

    Attributes:
        obj (str): The direct object to collect.
        other (str): The indirect object to collect.
        room (Room): The room to collect the items from.
    """

    def __init__(self, obj, other, room):
        self.obj = obj
        self.other = other
        self.room = room
        self.entities = []

    def collect(self):
        """Collect all objects that match the obj text.

        Returns:
            list of Entities: A list with all the entities that could
                be a match for the obj.
        """
        self.room.accept(self)
        if self.room in self.entities:
            self.entities.remove(self.room)
        return self.entities

    def visit_entity(self, entity):
        """Visit an Entity."""
        if entity.spec.name.lower().find(self.obj) > -1:
            self.entities.append(entity)
        # In the future??? Split the obj text into words
        # count how many words are present in a name or a description
        # add the count and the entity if there is at least one.
        # Then in the action resolver one can decide if there is a best match
        # that can be used only or if a menu is needed. Also, should check if
        # small words are being ignored, and consider if it should match whole
        # words or just part of words.

    def visit_container(self, container):
        """Visit a Container."""
        self.visit_entity(container)
        for item in container:
            item.accept(self)

    def visit_room(self, room):
        """Visit a Room"""
        self.visit_container(room)

    # Need a visit for character to deal with equipment.
    def visit_character(self, character):
        """Visit a Character"""
        for equipment in character.equipped:
            equipment.accept(self)

    def visit_player(self, player):
        """Visit a Player"""
        self.visit_container(player)
        self.visit_character(player)

    def visit_equipment(self, equipment):
        """Visit Equipment"""
        self.visit_entity(equipment)

    def visit_npc(self, npc):
        """Visit an Npc."""
        self.visit_entity(npc)


class EntityCollectorFactory:  # pylint: disable=too-few-public-methods
    """Factory to make an entity collector."""

    def make(self, obj, other, entity):  # pylint: disable=no-self-use
        """Makes an entity collector.

        Args:
            See EntityCollector Attributes.

        Returns:
            EntityCollector: The new entity collector.
        """
        return EntityCollector(obj, other, entity)


class EntityTypeCollector:
    """A Collector that will collect all entities in from a list of types.

    Attributes:
        types (list): List of type names (str) to collect.
        entity (Entity): An entity to collect or start collection with.
        results (list): List of the entities that are of the given types.

    Returns:
        The list of results.
    """

    def __init__(self, types, entity):
        self.types = types
        self.entity = entity
        self.results = []

    def collect(self):
        """Collect all entities of the given types from a given entity."""
        self.entity.accept(self)
        return self.results

    def visit_entity(self, entity):
        """Visit an Entity"""
        if 'entity' in self.types:
            self.results.append(entity)

    def visit_container(self, entity):
        """Visit a Container"""
        if 'container' in self.types:
            self.results.append(entity)
        self._collect_all(entity)

    def visit_player(self, entity):
        """Visit a Player"""
        if 'player' in self.types:
            self.results.append(entity)
        self._collect_all(entity)
        self._collect_equipped(entity)

    def visit_npc(self, entity):
        """Visit an Npc"""
        if 'npc' in self.types:
            self.results.append(entity)
        self._collect_all(entity)
        self._collect_equipped(entity)

    def visit_room(self, entity):
        """Visit a Room"""
        if 'room' in self.types:
            self.results.append(entity)
        self._collect_all(entity)

    def visit_equipment(self, entity):
        """Visit Equipment"""
        if 'equipment' in self.types:
            self.results.append(entity)

    def _collect_all(self, container):
        """Visit all sub entities of a given Container."""
        for item in container:
            item.accept(self)

    def _collect_equipped(self, character):
        """Visit all equipped items of a Character."""
        for item in character.equipped:
            item.accept(self)


class EntityIdCollector:
    """Collects an item with matching id looking in a given container
    and its sub containers.

    Attributes:
        obj_id (str): The id of the object to find.
        container (Container): The container to start looking in.
        result (Entity): The result of the search. The Entity with the
            given obj_id or None if no entity has the given obj_id.

    Returns:
        Entity: The Entity with the given obj_id if it is found,
            otherwise None."""

    def __init__(self, obj_id, container):
        self.obj_id = obj_id
        self.container = container
        self.result = None

    def collect(self):
        """Collect the desired Entity by ID."""
        self.container.accept(self)
        return self.result

    def visit_entity(self, entity):
        """If the entity has the matching ID set it as the result."""
        if entity.spec.id == self.obj_id:
            self.result = entity

    def visit_container(self, container):
        """Visit a Container."""
        self.visit_entity(container)
        for item in container:
            if self.result is None:
                item.accept(self)
            else:
                break

    def visit_room(self, room):
        """Visit a Room."""
        self.visit_container(room)

    def visit_character(self, character):
        """Visit a Character."""
        self.visit_container(character)
        for item in character.equipped:
            if self.result is None:
                item.accept(self)
            else:
                break

    def visit_player(self, player):
        """Visit a Player"""
        self.visit_character(player)

    def visit_npc(self, npc):
        """Visit an Npc"""
        self.visit_character(npc)

    def visit_equipment(self, equipment):
        """Visit Equipment."""
        self.visit_entity(equipment)

    def visit_world(self, world):
        """Visit a World."""
        if self.obj_id in world.entities:
            self.result = world.entities[self.obj_id]
