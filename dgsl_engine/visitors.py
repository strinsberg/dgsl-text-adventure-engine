"""Visitors for Collecting entities and for connecting game objects."""
from . import event_factory
from . import interaction as inter

# Should think about catching key errors here incase the world editor fails
# to provide all we need or a file is edited by hand and a mistake is made
# Or some kind of validation should be done of the world before attempting to
# load it. Make sure all objects are complete and that there are no cycles.


class EntityConnector:
    """Visitor to connect entities when building a world.

    Adds the references for the items contained to the appropriate
    entities.

    Attributes:
        entity_json (dict): A collection of all the json blueprints for
            entity and events.
        world (World): The world with all the Entity objects.
    """

    def __init__(self, entity_json, world):
        self.entity_json = entity_json
        self.world = world

    def connect(self, entity):
        """Add the events and entities that are connected to the entity."""
        self._connect_events(entity)
        entity.accept(self)

    def visit_entity(self, entity):
        """Do nothing. Entities have no events and already had events
        connected."""

    def visit_container(self, container):
        """Connect a container to its events and entities."""
        self._connect_items(container)

    def visit_room(self, room):
        """Connect a room to its events and entities."""
        self.visit_container(room)

    def visit_character(self, character):
        """Connect a character to its events and entities."""
        self.visit_container(character)
        # self.connect_equipment(character)

    def visit_equipment(self, equipment):
        """Do nothing. Equipment has no events and already had events
        connected."""

    def visit_npc(self, npc):
        """Connect a npc to its events and entities."""
        self.visit_character(npc)

    def visit_player(self, player):
        """Connect a player to its events and entities."""
        self.visit_character(player)

    def _connect_events(self, entity):
        """connect an entity to its events."""
        for event_json in self.entity_json['events']:
            event_id = event_json['id']
            event_verb = event_json['verb']
            event = self.world.events[event_id]
            entity.events.add(event_verb, event)

    def _connect_items(self, container):
        """connect an container to its items."""
        for item in self.entity_json['items']:
            item_id = item['id']
            entity = self.world.entities[item_id]
            container.add(entity)


class EventConnector:
    """Visitor to connect events when building a world.

    Connects all the events to the entities and events they are
    connected to.

    Attributes:
        entity_json (dict): A collection of all the json blueprints for
            entity and events.
        world (World): The world with all the Entity objects.
        world_json (dict): The blueprint for the world.
    """

    def __init__(self, event_json, world, world_json):
        self.event_json = event_json
        self.world = world
        self.world_json = world_json

    def connect(self, event):
        """Add all the items and events connected to the given item."""
        self._connect_subjects(event)
        event.accept(self)

    def visit_event(self, event):
        """Do Nothing. Single events have nothing connected to them."""

    def visit_move(self, move):
        """Connect the destination for the move event."""
        dest_id = self.event_json['destination']['id']
        destination = self.world.entities[dest_id]
        move.destination = destination

    def visit_give(self, give):
        """Connect the entity to transfer the item from."""
        owner_id = self.event_json['item_owner']['id']
        owner = self.world.entities[owner_id]
        give.item_owner = owner

    def visit_take(self, take):
        """Connect the entity to transfer the item to."""
        new_owner_id = self.event_json['new_owner']['id']
        new_owner = self.world.entities[new_owner_id]
        take.new_owner = new_owner

    def visit_toggle(self, toggle):
        """Connect the target of the toggle event."""
        target_id = self.event_json['target']['id']
        target = self.world.entities[target_id]
        toggle.target = target

    def visit_group(self, group):
        """Connect all the events in a group."""
        for obj in self.event_json['events']:
            event_id = obj['id']
            event = self.world.events[event_id]
            group.add(event)

    def visit_conditional(self, conditional):
        """Connect the event's condition and events."""
        success_id = self.event_json['success']['id']
        fail_id = self.event_json['failure']['id']
        cond_id = self.event_json['condition']['id']

        conditional.success = self.world.events[success_id]
        conditional.failure = self.world.events[fail_id]
        conditional.condition = event_factory.make_condition(
            self.world_json[cond_id], self.world)

    def visit_interaction(self, interaction):
        """Connect the events to the interaction."""
        for opt in self.event_json['options']:
            opt_json = self.world_json[opt['id']]
            self._connect_option(interaction, opt_json)

    def _connect_subjects(self, event):
        """Connect observers to an event."""
        for sub in self.event_json['subjects']:
            subject = self.world.events[sub['id']]
            event.register(subject)

    def _connect_option(self, interaction, opt_json):
        """Create and connect options to an interaction."""
        text = opt_json['text']
        event_id = opt_json['event']['id']
        event = self.world.events[event_id]

        if opt_json['type'] == 'conditional_option':
            cond_id = opt_json['condition']['id']
            condition = event_factory.make_condition(
                self.world_json[cond_id], self.world)
            interaction.add(inter.ConditionalOption(text, event, condition))
        else:
            interaction.add(inter.Option(text, event))
