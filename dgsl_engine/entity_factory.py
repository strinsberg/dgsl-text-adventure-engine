"""Module for Entity factory and supporting functions."""
from . import entity_base
from . import entity_containers
from . import exceptions
from . import equipment


class EntityFactory:  # pylint: disable=too-few-public-methods
    """Factory to create new entities from json objects of entity
    information."""

    def new(self, obj):  # pylint: disable=no-self-use
        """Create a new entity from an entity json.

        Args:
            obj (dict): A json object of entity info.

        Returns:
            Entity: The new entity.
        """
        try:
            type_ = obj['type']
            id_ = obj['id']
            if type_ == 'entity':
                entity = entity_base.Entity(id_)
            elif type_ == 'container':
                entity = entity_containers.Container(id_)
            elif type_ == 'room':
                entity = entity_containers.Room(id_)
            elif type_ == 'player':
                entity = entity_containers.Player(id_)
            elif type_ == 'npc':
                entity = entity_containers.Npc(id_)
            elif type_ == 'equipment':
                entity = equipment.Equipment(id_)
                _setup_equipment(entity, obj)
            else:
                raise exceptions.InvalidParameterError(
                    "Error: invalid obj of type " + type_)

            _setup_entity(entity, obj)

        except KeyError as err:
            raise exceptions.InvalidParameterError(
                "Error: object " + obj['name'] + " is not complete: " +
                str(err))

        return entity


def _setup_entity(entity, obj):
    entity.spec.name = obj['name']
    entity.spec.description = obj['description']

    if obj['type'] not in ['room', 'player']:
        entity.states.active = num_to_bool(obj['active'])
        entity.states.obtainable = num_to_bool(obj['obtainable'])
        entity.states.hidden = num_to_bool(obj['hidden'])


def _setup_equipment(entity, obj):
    entity.protects = obj['protects']
    entity.slot = obj['slot']
    entity.must_equip = obj['must_equip']


def num_to_bool(num):
    """Turns a number into a bool."""
    return num != 0
