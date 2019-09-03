"""Game world and supporting functions."""
from . import entity_factory
from . import event_factory
from . import visitors


class World:
    """A Game world that holds entities and the player.

    Attributes:
        details (WorldDetails): The information about the world.
        player (Player): The player character.
        entities (dict): All the entities in the world. Keys are entity IDs.
        events (dict): All the events in the world. Keys are event IDs.
    """

    def __init__(self):
        self.details = None
        self.player = None
        self.entities = {}
        self.events = {}

    def add_entity(self, entity):
        """Adds a given entity to the worlds entities."""
        self.entities[entity.spec.id] = entity

    def add_event(self, event):
        """Adds a given event to the worlds events."""
        self.events[event.id] = event

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_world(self)


class WorldDetails:  # pylint: disable=too-few-public-methods
    """World details data.

    Attributes:
        name (str): The worlds name
        welcome (str): Information about the world.
        opening (str): The text to start the story.
        version (str): The worlds version.
    """

    def __init__(self, name, welcome, opening, version):
        self.name = name
        self.welcome = welcome
        self.opening = opening
        self.version = version


class WorldFactory:  # pylint: disable=too-few-public-methods
    """Creates a new world from a compatible json blueprint.

    Attributes:
        entity_factory: A factory object for creating entities from
            entity json blueprints.
        event_factory: A factory object for creating events from
            event json blueprints.
    """

    def __init__(self):
        self.entity_factory = entity_factory.EntityFactory()
        self.event_factory = event_factory.EventFactory()

    def new(self, world_json):
        """Creates and returns a new World object from the given
        json blueprint.
        """
        new_world = World()

        self._create_objects(new_world, world_json)
        _connect_objects(new_world, world_json)
        _setup_world(new_world, world_json)

        return new_world

    def _create_objects(self, new_world, world_json):
        """Creates ad adds entities and events to the world.

        just provides them with the information to make the objects, but
        does not add entities or events that they contain yet.

        Some objects like conditions and options are not created until
        connection time.
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
            elif create_later(obj):
                pass
            else:
                raise AttributeError(  # should use different error type
                    "*** Error: World creator does not recognize type: "
                    + obj['type'] + " ***")


def _connect_objects(new_world, world_json):
    """Connects all the objects in a world together.

    Some objects like options and conditions are created when
    the objects that need them are connected.
    """
    for id_ in world_json['objects']:
        obj = world_json['objects'][id_]
        if is_entity(obj):
            conn = visitors.EntityConnector(obj, new_world)
            entity = new_world.entities[id_]
            conn.connect(entity)
            if obj['type'] == 'player':
                start_room = new_world.entities[obj['start']['id']]
                start_room.add(entity)
        elif is_event(obj):
            conn = visitors.EventConnector(
                obj, new_world, world_json['objects'])
            event = new_world.events[id_]
            conn.connect(event)


def _setup_world(new_world, world_json):
    """Adds the world details to a world."""
    details = WorldDetails(
        world_json['name'], world_json['welcome'],
        "You are playing this game!", world_json['version'])
    new_world.details = details
    #new_world.details.opening = world_json['opening']


def is_entity(obj):
    """Checks if json blueprint is an entity."""
    return obj['type'] in ['entity', 'container', 'room', 'player', 'equipment', 'npc']


def is_event(obj):
    """Checks if json blueprint is an entity."""
    return obj['type'] in ['inform', 'event', 'move', 'give', 'end_game',
                           'take', 'toggle_active',
                           'toggle_obtainable', 'toggle_hidden', 'group',
                           'ordered', 'conditional', 'interaction']


def create_later(obj):
    """Checks if json blueprint is an object that has creation delayed
    until connection time."""
    return obj['type'] in ['option', 'conditional_option', 'hasItem',
                           'protected', 'question', 'is_active']
