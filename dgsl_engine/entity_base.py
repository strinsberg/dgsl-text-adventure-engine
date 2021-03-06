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
        owner (Container): The container that the entity is in.
    """

    def __init__(self, obj_id):
        self.spec = EntitySpec(obj_id)
        self.states = EntityStates()
        self.events = EntityEvents()
        self.owner = None

    def describe(self):
        """Gives a description of the entity.

        Can be extended to give more detailed descriptions of complex
        entities.

        Returns:
            str: The entity's description.
        """
        return self.spec.description

    def accept(self, visitor):
        """Accepts the visitor and calls the appropriate visit."""
        visitor.visit_entity(self)

    def __repr__(self):
        return "<Entity '{}', Name: '{}'>".format(self.spec.id, self.spec.name)


class EntitySpec:  # pylint: disable=too-few-public-methods
    """The textual details of an Entity.

    Attributes:
        id (str): A unique identifer.
        name (str): A name or brief description.
        description (str): A more detailed description.
    """

    def __init__(self, obj_id):
        self.id = obj_id  # pylint: disable=invalid-name
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

    def toggle_active(self):
        """Toggles the active state."""
        if self.active:
            self.active = False
        else:
            self.active = True

    def toggle_obtainable(self):
        """Toggles the obtainable state."""
        if self.obtainable:
            self.obtainable = False
        else:
            self.obtainable = True

    def toggle_hidden(self):
        """Toggles the hidden state."""
        if self.hidden:
            self.hidden = False
        else:
            self.hidden = True


class EntityEvents:
    """The responses to player actions.

    Events are identified by a verb. If the player interacts with the
    entity using a verb that the entity has an event for it can be
    executed (if active and not hidden). Events can also be stored with
    verbs that are not likely to be typed by the player if they are
    triggered by other events instead of player actions.

    Attributes:
        events (dict <str, :class:`Event <dgsl_engine.event_base.Event>`>):
            Events attached to an entity.
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


class Inventory:
    """Inventory for holding entities.

    Can be used in for loops to iterate over all items it contains.

    ::

        for item in inventory:
            print(item)

    Attributes:
        items (dict <str, :class:`Entity <dgsl_engine.entity_base.Entity>`>):
            Entities in the inventory.
    """

    def __init__(self):
        self.items = {}

    def __iter__(self):
        for k in self.items:
            yield self.items[k]

    def empty(self):
        """Returns true if the inventory is empty."""
        return len(self.items) == 0

    def add(self, item):
        """Add an Entity to the inventory.

        Args:
            item (Entity): An Entity.

        Returns:
            bool: True if the Entity is added, False if the entity is
            already there.
        """
        if item.spec.id not in self.items:
            self.items[item.spec.id] = item
            return True
        return False

    def remove(self, item_id):
        """Remove an Entity.

        Args:
            item_id (str): The id of the entity to remove.

        Returns:
            Entity: The Entity with the given id. None if the Entity is
            not in the inventory.
        """
        return self.items.pop(item_id, None)

    def has_item(self, item_id):
        """Checks to see if an Entity with the given id is in the inventory.

        Args:
            item_id (str): The id of the entity to find.

        Returns:
            bool: True if the Entity is there, False otherwise.
        """
        return item_id in self.items


class Equipped:
    """An inventory of worn equipment for a Character.

    Attributes:
        owner (Character): The character that is wearing the equipment."
        equipment (dict): The worn equipment. The keys are the name of
            the slot the equipment is being worn in and the values are
            the equipment.
    """

    def __init__(self, owner):
        self.owner = owner
        self.equipment = {}

    def __iter__(self):
        for k in self.equipment:
            yield self.equipment[k]

    def empty(self):
        """Returns True if the equipment is empty."""
        return len(self.equipment) == 0

    def equip(self, equipment):
        """Equips the given equipment.

        Args:
            equipment (Equipment): The piece of equipment to equip.

        Returns:
            Equipment: If there is a piece of equipment already equipped
                in the slot needed it is returned, otherwise None.
        """
        slot = equipment.slot
        old = None
        if slot in self.equipment:
            old = self.remove(slot)
        self.equipment[slot] = equipment
        equipment.owner = self.owner
        equipment.equipped = True
        return old

    def remove(self, slot):
        """Removes the piece of equipment from the given slot.

        Args:
            slot (str): The name of the slot to remove equipment from.

        Returns:
            Equipment: The piece of equipment in the given slot. If the
                slot is empty then None."""
        old = None
        if slot in self.equipment:
            old = self.equipment[slot]
            old.owner = None
            old.equipped = False
            del self.equipment[slot]
        return old

    def wearing(self, equip):
        """Check to see if a piece of equipment is being worn.

        Args:
            equip (Equipment): The equipment to check for.

        Returns:
            str: The slot the equipment is in, otherwise None."""
        for slot, item in self.equipment.items():
            if item.spec.name == equip.spec.name:
                return slot
        return None

    def get(self, slot):
        """Returns the equipment in a given slot, or None if the slot is
        empty.
        """
        if slot in self.equipment:
            return self.equipment[slot]
        return None
