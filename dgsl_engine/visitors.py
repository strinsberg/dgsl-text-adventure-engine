"""Visitors for Collecting entities and for connecting game objects."""
from . import event_factory
from . import interaction as inter


class EntityCollector:
    """Visitor that collects all items that match with player input.

    Attributes:
        obj (str): The direct object to collect.
        other (str): The indirect object to collect.
        room (Room): The room to collect the items from.
    """

    def __init__(self, obj, other, room):
        self.obj = obj
        self.other = other
        self.room = room
        self.entities = []

    def collect(self):
        """Collect all objects that match the obj text.

        Returns:
            list of Entities: A list with all the entities that could
                be a match for the obj.
        """
        self.room.accept(self)
        if self.room in self.entities:
            self.entities.remove(self.room)
        return self.entities

    def visit_entity(self, entity):
        """Visit and entity."""
        if entity.spec.name.find(self.obj) > -1:
            self.entities.append(entity)

    def visit_container(self, container):
        """Visit a container."""
        self.visit_entity(container)
        for item in container:
            item.accept(self)

    def visit_room(self, room):
        """empty"""
        self.visit_container(room)

    # Need a visit for character to deal with equipment.
    def visit_character(self, character):
        """empty"""
        for equipment in character.equipped:
            equipment.accept(self)

    def visit_player(self, player):
        """empty"""
        self.visit_container(player)
        self.visit_character(player)

    def visit_equipment(self, equipment):
        """empty"""
        self.visit_entity(equipment)

    def visit_npc(self, npc):
        """Visit an Npc."""
        self.visit_entity(npc)


class EntityCollectorFactory:  # pylint: disable=too-few-public-methods
    """Factory to make an entity collector."""

    def make(self, obj, other, entity):  # pylint: disable=no-self-use
        """Makes an entity collector.

        Args:
            See EntityCollector Attributes.

        Returns:
            EntityCollector: The new entity collector.
        """
        return EntityCollector(obj, other, entity)


class EntityTypeCollector:
    """this is a little gross, better to make a base collector with all
    the methods implemented with pass. then make specific type collectors
    or something with just their method implemented. though this would not
    work easily for multiple types."""

    def __init__(self, types, entity):
        self.types = types
        self.entity = entity
        self.results = []

    def collect(self):
        """empty"""
        self.entity.accept(self)
        return self.results

    def visit_entity(self, entity):
        """empty"""
        if 'entity' in self.types:
            self.results.append(entity)

    def visit_container(self, entity):
        """empty"""
        if 'container' in self.types:
            self.results.append(entity)
        self._collect_all(entity)

    def visit_player(self, entity):
        """empty"""
        if 'player' in self.types:
            self.results.append(entity)
        self._collect_all(entity)
        self._collect_equipped(entity)

    def visit_npc(self, entity):
        """empty"""
        if 'npc' in self.types:
            self.results.append(entity)
        self._collect_all(entity)
        self._collect_equipped(entity)

    def visit_room(self, entity):
        """empty"""
        if 'room' in self.types:
            self.results.append(entity)
        self._collect_all(entity)

    def visit_equipment(self, entity):
        """empty"""
        if 'equipment' in self.types:
            self.results.append(entity)

    def _collect_all(self, container):
        """empty"""
        for item in container:
            item.accept(self)

    def _collect_equipped(self, character):
        """empty"""
        for item in character.equipped:
            item.accept(self)

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
        """Some info."""
        self._connect_events(entity)
        entity.accept(self)

    def visit_entity(self, entity):
        """Some info."""

    def visit_container(self, container):
        """Some info."""
        self._connect_items(container)

    def visit_room(self, room):
        """empty"""
        self.visit_container(room)

    def visit_character(self, character):
        """empty"""
        self.visit_container(character)
        # self.connect_equipment(character)

    def visit_player(self, player):
        """empty"""
        self.visit_character(player)

    def visit_npc(self, npc):
        """empty"""
        self.visit_character(npc)

    def _connect_events(self, entity):
        """empty"""
        for event_json in self.entity_json['events']:
            event_id = event_json['id']
            event_verb = event_json['verb']
            event = self.world.events[event_id]
            entity.events.add(event_verb, event)

    def _connect_items(self, container):
        """empty"""
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
        """Some info."""
        self._connect_subjects(event)
        event.accept(self)

    def visit_event(self, event):
        """Some info."""

    def visit_move(self, move):
        """Some info."""
        dest_id = self.event_json['destination']['id']
        destination = self.world.entities[dest_id]
        move.destination = destination

    def visit_give(self, give):
        """empty"""
        owner_id = self.event_json['item_owner']['id']
        owner = self.world.entities[owner_id]
        give.item_owner = owner

    def visit_take(self, take):
        """empty"""
        new_owner_id = self.event_json['new_owner']['id']
        new_owner = self.world.entities[new_owner_id]
        take.new_owner = new_owner

    def visit_toggle(self, toggle):
        """empty"""
        target_id = self.event_json['target']['id']
        target = self.world.entities[target_id]
        toggle.target = target

    def visit_group(self, group):
        """empty"""
        for obj in self.event_json['events']:
            event_id = obj['id']
            event = self.world.events[event_id]
            group.add(event)

    def visit_conditional(self, conditional):
        """empty"""
        success_id = self.event_json['success']['id']
        fail_id = self.event_json['failure']['id']
        conditional.success = self.world.events[success_id]
        conditional.failure = self.world.events[fail_id]
        conditional.condition = event_factory.make_condition(
            self.event_json['condition'])

    def visit_interaction(self, interaction):
        """empty"""
        for opt in self.event_json['options']:
            self._connect_option(interaction, opt)

    def _connect_subjects(self, event):
        """empty"""
        for sub in self.event_json['subjects']:
            subject = self.world.events[sub['id']]
            event.register(subject)

    def _connect_option(self, interaction, opt_json):
        """empty"""
        text = opt_json['text']
        event_id = opt_json['event']['id']
        event = self.world.events[event_id]

        if opt_json['type'] == 'conditional':
            condition = event_factory.make_condition(opt_json['condition'])
            interaction.add(inter.ConditionalOption(text, event, condition))
        else:
            interaction.add(inter.Option(text, event))
