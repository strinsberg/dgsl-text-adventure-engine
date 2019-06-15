"""
Base Event as well as supporting classes and functions.
"""


class Entity:
    """An entity that exists in the game world.
    
    Attributes:
        spec (EntitySpec): Details about the entity.
        states (EntityStates): The entities various states.
        events (EntityEvents): Events attached to the entity that can be
            triggered by player interactions.
    """

    def __init__(self, obj_id):
        self.spec = EntitySpec(obj_id)
        self.states = EntityStates()
        self.events = EntityEvents()

    def describe(self):
        """Gives a description of the entity.
        
        Can be extended to give more detailed descriptions of complex
        entities.
        
        Returns:
            str: The entity's description.
        """
        return self.spec.description


class EntitySpec:
    """The textual details of an Entity.
    
    Attributes:
        id (str): A unique identifer.
        name (str): A name or brief description.
        description (str): A more detailed description.
    """

    def __init__(self, obj_id):
        self.id = obj_id
        self.name = "Null"
        self.description = "Null"


class EntityStates:
    """The various states of an Entity.
    
    Attributes:
        active (bool): If an entity will respond to interactions.
        obtainable (bool): If an entity can be picked up.
        hidden (bool): If an entity can be seen and interacted with.
    """

    def __init__(self):
        self.active = True
        self.obtainable = True
        self.hidden = False


class EntityEvents:
    """The responses to player actions.
    
    Events are identified by a verb. If the player interacts with the
    entity using a verb that the entity has an event for it can be
    executed (if active and not hidden). Events can also be stored with
    verbs that are not likely to be typed by the player if they are
    triggered by other events instead of player actions.

    Attributes:
        events (dict <str, :class:`Event <dgsl_engine.event_base.Event>`>): Events
            attached to an entity.
    """

    def __init__(self):
        self.events = {}

    def add(self, verb, event):
        """Adds an event with for a given verb.

        Args:
            verb (str): The verb to associate the event with.
            event (Event): The Event.

        Returns:
            bool: True if the event is added. False if there is
            already an event associated to the verb.

        """
        if verb not in self.events:
            self.events[verb] = event
            return True

        return False

    def execute(self, verb, entity):
        """Executes the event on the given entity and returns the result.

        Args:
            verb (str): The verb of the event to execute.
            entity (Entity): The entity affected by the event.

        Returns:
            str: A description of the results.
        """
        return self.events[verb].execute(entity)

    def has_event(self, verb):
        """Checks to see if the given verb has an associated event.

        Args:
          verb (str): The verb to check.

        Returns:
            bool: True if there is an event associated to the verb,
            False otherwise.
        """
        return verb in self.events