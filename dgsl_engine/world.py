"""Game world and supporting functions."""
from . import entity_factory
from . import event_factory
from . import visitors


class World:
    """A Game world that holds entities and the player."""

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
        """

        Args:
          entity: 

        Returns:

        """
        self.entities[entity.spec.id] = entity

    def add_event(self, event):
        """

        Args:
          event: 

        Returns:

        """
        self.events[event.id] = event


class WorldFactory:
    """Creates a new world from a compatible json object."""

    def __init__(self):
        self.entity_factory = entity_factory.EntityFactory()
        self.event_factory = event_factory.EventFactory()

    def new(self, world_json):
        """

        Args:
          world_json: 

        Returns:

        """
        new_world = World()

        self._create_objects(new_world, world_json)
        self._connect_objects(new_world, world_json)
        self._setup_world(new_world, world_json)

        return new_world

    def _create_objects(self, new_world, world_json):
        """

        Args:
          new_world: 
          world_json: 

        Returns:

        """
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
        """

        Args:
          new_world: 
          world_json: 

        Returns:

        """
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
        """

        Args:
          new_world: 
          world_json: 

        Returns:

        """
        new_world.name = world_json['name']
        new_world.version = world_json['version']
        new_world.welcome = world_json['welcome']
        #world.opening = world_json['opening']
        #world.player_title = world_json['player_title']


def is_entity(obj):
    """

    Args:
      obj: 

    Returns:

    """
    return obj['type'] in ['entity', 'container', 'room', 'player', 'equipment']


def is_event(obj):
    """

    Args:
      obj: 

    Returns:

    """
    return obj['type'] in ['inform', 'move', 'transfer', 'toggle_active',
                           'toggle_obtainable', 'toggle_hidden', 'group',
                           'ordered', 'conditional', 'interaction']
