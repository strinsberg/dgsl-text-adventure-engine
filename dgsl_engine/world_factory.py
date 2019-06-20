from . import entity_containers as containers


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

        for obj in world_json['objects']:
            if obj['type'] == 'player':
                world.player = containers.Player(obj['id'])
                set_up_entity(world.player, obj)
            elif is_entity(obj):
                world.entities[obj['id']] = new_entity(obj)
            elif is_event(obj):
                world.events[obj['id']] = new_event(obj)

        for obj in world_json['objects']:
            if is_entity(obj):
                self._connect_entity(obj)
            elif is_event(obj):
                self._connect_event(obj)

        world.name = world_json['name']
        world.version = world_json['version']
        world.welcome = world_json['welcome']
        world.opening = world_json['opening']
        world.player_title = world_json['player_title']

        return world

    def _connect_entity(self, obj):
        pass

    def _connect_event(self, obj):
        pass


def is_entity(obj):
    return True


def is_event(obj):
    return True


def new_entity(obj):
    return {}


def new_event(obj):
    return {}


def set_up_entity(entity, obj):
    return {}


def set_up_event(entity, obj):
    return {}
