from functools import singledispatch
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

    def __init__(self, entity, world):
        pass

    def connect(self):
        pass

    def visit_entity(self, entity):
        pass

    def visit_container(self, container):
        pass


class EventConnector:
    """Visitor to connect events when building a world."""

    def __init__(self, event, world):
        pass

    def visit_event(self, event):
        pass

    def visit_move(self, move):
        pass


class ConnectorFactory:
    @singledispatch
    def make(self, obj, world):
        pass

    @make.register(entity_base.Entity)
    def _(self, entity, world):
        pass

    @make.register(event_base.Event)
    def _(self, event, world):
        pass