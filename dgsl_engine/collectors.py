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
        """Visit and entity."""
        if (entity.spec.name.find(self.obj) > -1
                or entity.spec.description.find(self.obj) > -1):
            self.entities.append(entity)
        # Split the obj text into words
        # count how many words are present in a name or a description
        # add the count and the entity if there is at least one.
        # Then in the action resolver one can decide if there is a best match
        # that can be used only or if a menu is needed. Also, should check if
        # small words are being ignored, and consider if it should match whole
        # words or just part of words.

    def visit_container(self, container):
        """Visit a container."""
        self.visit_entity(container)
        for item in container:
            item.accept(self)

    def visit_room(self, room):
        """empty"""
        self.visit_container(room)

    # Need a visit for character to deal with equipment.
    def visit_character(self, character):
        """empty"""
        for equipment in character.equipped:
            equipment.accept(self)

    def visit_player(self, player):
        """empty"""
        self.visit_container(player)
        self.visit_character(player)

    def visit_equipment(self, equipment):
        """empty"""
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
    """this is a little gross, better to make a base collector with all
    the methods implemented with pass. then make specific type collectors
    or something with just their method implemented. though this would not
    work easily for multiple types."""

    def __init__(self, types, entity):
        self.types = types
        self.entity = entity
        self.results = []

    def collect(self):
        """empty"""
        self.entity.accept(self)
        return self.results

    def visit_entity(self, entity):
        """empty"""
        if 'entity' in self.types:
            self.results.append(entity)

    def visit_container(self, entity):
        """empty"""
        if 'container' in self.types:
            self.results.append(entity)
        self._collect_all(entity)

    def visit_player(self, entity):
        """empty"""
        if 'player' in self.types:
            self.results.append(entity)
        self._collect_all(entity)
        self._collect_equipped(entity)

    def visit_npc(self, entity):
        """empty"""
        if 'npc' in self.types:
            self.results.append(entity)
        self._collect_all(entity)
        self._collect_equipped(entity)

    def visit_room(self, entity):
        """empty"""
        if 'room' in self.types:
            self.results.append(entity)
        self._collect_all(entity)

    def visit_equipment(self, entity):
        """empty"""
        if 'equipment' in self.types:
            self.results.append(entity)

    def _collect_all(self, container):
        """empty"""
        for item in container:
            item.accept(self)

    def _collect_equipped(self, character):
        """empty"""
        for item in character.equipped:
            item.accept(self)


class EntityIdCollector:
    """Collects an item with mathcing id. Will find it anywhere it is."""

    def __init__(self, obj_id, container):
        self.obj_id = obj_id
        self.container = container
        self.result = None

    def collect(self):
        """empty"""
        self.container.accept(self)
        return self.result

    def visit_entity(self, entity):
        """empty"""
        if entity.spec.id == self.obj_id:
            self.result = entity

    def visit_container(self, container):
        """empty"""
        self.visit_entity(container)
        for item in container:
            if self.result is None:
                item.accept(self)
            else:
                break

    def visit_room(self, room):
        """empty"""
        self.visit_container(room)

    def visit_character(self, character):
        """empty"""
        self.visit_container(character)
        for item in character.equipped:
            if self.result is None:
                item.accept(self)
            else:
                break

    def visit_player(self, player):
        """empty"""
        self.visit_character(player)

    def visit_npc(self, npc):
        """empty"""
        self.visit_character(npc)

    def visit_equipment(self, equipment):
        """empty"""
        self.visit_entity(equipment)
