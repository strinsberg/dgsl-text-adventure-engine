from . import entity_containers as containers
from . import entity_factory
from . import event_factory


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


class WorldFactory:
    def new(self, world_json):
        world = World()

        self._create_objects(world, world_json)
        self._connect_objects(world, world_json)
        self._setup_world(world, world_json)

        return world

    def _create_objects(self, world, world_json):
        for obj in world_json['objects']:
            if obj['type'] == 'player':
                world.player = containers.Player(obj['id'])
                entity_factory.setup_entity(world.player, obj)
            elif is_entity(obj):
                world.entities[obj['id']] = entity_factory.new_entity(obj)
            elif is_event(obj):
                world.events[obj['id']] = event_factory.new_event(obj)

    def _connect_objects(self, world, world_json):
        for obj in world_json['objects']:
            if is_entity(obj):
                self._connect_entity(obj)
            elif is_event(obj):
                self._connect_event(obj)

    def _setup_world(self, world, world_json):
        world.name = world_json['name']
        world.version = world_json['version']
        world.welcome = world_json['welcome']
        #world.opening = world_json['opening']
        #world.player_title = world_json['player_title']

    def _connect_entity(self, obj):
        pass

    def _connect_event(self, obj):
        pass


def is_entity(obj):
    return obj['type'] in ['entity', 'container', 'room', 'player']


def is_event(obj):
    return obj['type'] in ['inform', 'move', 'toggle', 'transfer']
