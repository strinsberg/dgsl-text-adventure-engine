"""Event factory to create new events from json event objects."""
from . import event_base
from . import event_single
from . import event_single_decorators as evs
from . import exceptions


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
                event = event_single.MoveEntity(id_)
            else:
                raise exceptions.InvalidParameterError(
                    "Error: invalid obj of type " + type_)

            return self._setup(event, obj)

        except KeyError as err:
            raise exceptions.InvalidParameterError(
                "Error: object is not complete: " + str(err))

    def _setup(self, event, obj):
        event.only_once = num_to_bool(obj['once'])
        return self._add_decorators(event, obj)

    def _add_decorators(self, event, obj):
        # Proabably split this into 2 methods or multiple private functions
        # to accomadate single and multiple decorators once they exist
        if 'message' in obj:
            decorated = evs.MessageDecorator(event, obj['message'])
        else:
            return event
        return decorated


def num_to_bool(num):
    """Turn a number into a bool."""
    return num != 0
