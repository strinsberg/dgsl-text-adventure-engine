from . import entity_containers as containers
from . import entity_factory
from . import event_factory
from . import visitors


class World:
    def __init__(self):
        self.name = "Untitled"
        self.welcome = "Welcome to my game!"
        self.opening = "You are in a very interesting place!"
        self.player_title = "Captain"
        self.version = "0.0.0"
        self.player = None
        self.entities = {}
        self.events = {}

    def add_entity(self, entity):
        self.entities[entity.spec.id] = entity

    def add_event(self, event):
        self.events[event.id] = event


class WorldFactory:
    def __init__(self):
        self.entity_factory = entity_factory.EntityFactory()
        self.event_factory = event_factory.EventFactory()

    def new(self, world_json):
        new_world = World()

        self._create_objects(new_world, world_json)
        self._connect_objects(new_world, world_json)
        self._setup_world(new_world, world_json)

        return new_world

    def _create_objects(self, new_world, world_json):
        objects = world_json['objects']
        for id_ in objects:
            obj = objects[id_]  # Because id, obj in objects is not working
            if is_entity(obj):
                entity = self.entity_factory.new(obj)
                new_world.add_entity(entity)
                if obj['type'] == 'player':
                    new_world.player = entity
            elif is_event(obj):
                new_world.add_event(self.event_factory.new(obj))

    def _connect_objects(self, new_world, world_json):
        for id_ in world_json['objects']:
            obj = world_json['objects'][id_]
            if is_entity(obj):
                conn = visitors.EntityConnector(obj, new_world)
                entity = new_world.entities[id_]
                conn.connect(entity)
                if obj['type'] == 'player':
                    start_room = new_world.entities[obj['start']]
                    start_room.add(entity)
            elif is_event(obj):
                conn = visitors.EventConnector(obj, new_world)
                event = new_world.events[id_]
                conn.connect(event)

    def _setup_world(self, new_world, world_json):
        new_world.name = world_json['name']
        new_world.version = world_json['version']
        new_world.welcome = world_json['welcome']
        #world.opening = world_json['opening']
        #world.player_title = world_json['player_title']


def is_entity(obj):
    return obj['type'] in ['entity', 'container', 'room', 'player']


def is_event(obj):
    return obj['type'] in ['inform', 'move', 'toggle', 'transfer']
