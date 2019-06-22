from . import entity_base
from . import entity_containers
from . import exceptions


class EntityFactory:
    def new(self, obj):
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
            else:
                raise exceptions.InvalidParameterError(
                    "Error: invalid obj of type " + type_)

            self._setup(entity, obj)

        except KeyError as err:
            raise exceptions.InvalidParameterError(
                "Error: object is not complete: " + str(err))

        return entity

    def _setup(self, entity, obj):
        entity.spec.name = obj['name']
        entity.spec.description = obj['description']

        if obj['type'] != 'room':
            entity.states.active = num_to_bool(obj['active'])
            entity.states.obtainable = num_to_bool(obj['obtainable'])
            entity.states.hidden = num_to_bool(obj['hidden'])


def num_to_bool(num):
    return num == 1