"""Event factory to create new events from json event objects."""
from . import event_base
from . import exceptions
from . import event_composites
from . import interaction


class EventFactory:
    """Event factory to create new events from json event objects."""

    def new(self, obj):
        """Create and return a new event from an event json.

        Args:
            obj (dict): A json object with information for an event.
        """
        try:
            type_ = obj['type']
            id_ = obj['id']
            if type_ in ['event',
                         'inform']:  # remove inform when editor is fixed
                event = event_base.Event(id_)
            elif type_ == 'move':
                event = event_base.MoveEntity(id_)
            elif type_ == 'give':
                event = event_base.Give(id_)
            elif type_ == 'take':
                event = event_base.Take(id_)
            elif type_ == 'toggle_active':
                event = event_base.ToggleActive(id_)
            elif type_ == 'toggle_obtainable':
                event = event_base.ToggleObtainable(id_)
            elif type_ == 'toggle_hidden':
                event = event_base.ToggleHidden(id_)
            elif type_ == 'group':
                event = event_composites.GroupEvent(id_)
            elif type_ == 'ordered':
                event = event_composites.OrderedGroup(id_)
            elif type_ == 'conditional':
                event = event_composites.ConditionalEvent(id_)
            elif type_ == 'interaction':
                event = interaction.Interaction(id_)
            else:
                raise exceptions.InvalidParameterError(
                    "Error: invalid obj of type " + type_)

            self._setup(event, obj)
            return event

        except KeyError as err:
            raise exceptions.InvalidParameterError(
                "Error: object is not complete: " + str(err))

    def _setup(self, event, obj):
        event.only_once = num_to_bool(obj['once'])
        if 'message' in obj:
            event.message = obj['message']


def num_to_bool(num):
    """Turn a number into a bool."""
    return num != 0
