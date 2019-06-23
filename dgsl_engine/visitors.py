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
            e = self.world.events[event_id]
            entity.events.add(event_verb, e)

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
        self._connect_subjects(event)
        event.accept(self)

    def visit_event(self, event):
        pass

    def visit_move(self, move):
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