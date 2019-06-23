from . import entity_base
from . import event_base


class EntityCollector:
    """Visitor that collects all items that match with player input."""

    def __init__(self, obj, other, room):
        self.obj = obj
        self.other = other
        self.room = room
        self.entities = []

    def collect(self):
        self.room.accept(self)
        if self.room in self.entities:
            # It would be better not to add it than to remove it
            # Maybe accept or visit could have an exclude
            self.entities.remove(self.room)
        return self.entities

    def visit_entity(self, entity):
        if entity.spec.name.find(self.obj) > -1:
            self.entities.append(entity)

    def visit_container(self, container):
        self.visit_entity(container)
        for item in container:
            item.accept(self)


class EntityCollectorFactory:
    def make(self, obj, other, entity):
        return EntityCollector(obj, other, entity)


class EntityConnector:
    """Visitor to connect entities when building a world."""

    def __init__(self, entity_json, world):
        self.entity_json = entity_json
        self.world = world

    def connect(self, entity):
        self._connect_events(entity)
        entity.accept(self)

    def visit_entity(self, entity):
        pass

    def visit_container(self, container):
        self._connect_items(container)

    def _connect_events(self, entity):
        for event in self.entity_json['events']:
            event_id = event['id']
            event_verb = event['verb']
            event = self.world.events[event_id]
            entity.events.add(event_verb, event)

    def _connect_items(self, container):
        for item in self.entity_json['items']:
            item_id = item['id']
            entity = self.world.entities[item_id]
            container.add(entity)


class EventConnector:
    """Visitor to connect events when building a world."""

    def __init__(self, event, world):
        pass

    def visit_event(self, event):
        pass

    def visit_move(self, move):
        pass
