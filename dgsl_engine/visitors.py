"""Visitors for Collecting entities and for connecting game objects."""


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
            # It would be better not to add it than to remove it
            # Maybe accept or visit could have an exclude
            self.entities.remove(self.room)
        return self.entities

    def visit_entity(self, entity):
        """Visit and entity."""
        if entity.spec.name.find(self.obj) > -1:
            self.entities.append(entity)

    def visit_container(self, container):
        """Visit a container."""
        self.visit_entity(container)
        for item in container:
            item.accept(self)

    def visit_npc(self, npc):
        """Visit an Npc."""
        self.visit_entity(npc)


class EntityCollectorFactory:
    """Factory to make an entity collector."""

    def make(self, obj, other, entity):
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

    def __init__(self, types, container):
        self.types = types
        self.container = container
        self.results = []

    def collect(self):
        for entity in self.container:
            entity.accept(self)
        return self.results

    def visit_entity(self, entity):
        if 'entity' in self.types:
            self.results.append(entity)

    def visit_container(self, entity):
        if 'container' in self.types:
            self.results.append(entity)

    def visit_player(self, entity):
        if 'player' in self.types:
            self.results.append(entity)

    def visit_npc(self, entity):
        if 'npc' in self.types:
            self.results.append(entity)

    def visit_equipment(self, entity):
        if 'equipment' in self.types:
            self.results.append(entity)

# Should think about catching key errors here incase the world editor fails
# to provide all we need or a file is edited by hand and a mistake is made
# Or aome kind of validation should be done of the world before attempting to
# load it. Make sure all objects are complete and that there are no cycles.


class EntityConnector:
    """Visitor to connect entities when building a world."""

    def __init__(self, entity_json, world):
        self.entity_json = entity_json
        self.world = world

    def connect(self, entity):
        """Some info."""
        self._connect_events(entity)
        entity.accept(self)

    def visit_entity(self, entity):
        """Some info."""

    def visit_container(self, container):
        """Some info."""
        self._connect_items(container)

    def _connect_events(self, entity):
        for event_json in self.entity_json['events']:
            event_id = event_json['id']
            event_verb = event_json['verb']
            event = self.world.events[event_id]
            entity.events.add(event_verb, event)

    def _connect_items(self, container):
        for item in self.entity_json['items']:
            item_id = item['id']
            entity = self.world.entities[item_id]
            container.add(entity)


class EventConnector:
    """Visitor to connect events when building a world."""

    def __init__(self, event_json, world):
        self.event_json = event_json
        self.world = world

    def connect(self, event):
        """Some info."""
        self._connect_subjects(event)
        event.accept(self)

    def visit_event(self, event):
        """Some info."""

    def visit_move(self, move):
        """Some info."""
        dest_id = self.event_json['destination']['id']
        destination = self.world.entities[dest_id]
        move.destination = destination

    def _connect_subjects(self, event):
        for sub in self.event_json['subjects']:
            subject = self.world.events[sub['id']]
            event.register(subject)

    # Add something like this when you add group events
    def _connect_events(self, group):  # pragma: no cover
        pass
