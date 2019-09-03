"""Event factory to create new events from json event objects."""
from . import event_base
from . import exceptions
from . import event_composites
from . import interaction
from . import conditions


class EventFactory:  # pylint: disable=too-few-public-methods
    """Event factory to create new events from json event objects."""

    # Turn this into 2 functions to try create single and group
    # events for the factory to return.
    def new(self, obj):  # pylint: disable=no-self-use,too-many-branches
        """Create and return a new event from an event json.

        Args:
            obj (dict): A json object with information for an event.

        Returns:
            Event: The newly constructed event.
        """
        try:
            type_ = obj['type']
            id_ = obj['id']
            if type_ in ['event']:
                event = event_base.Event(id_)
            elif type_ == 'move':
                event = event_base.MoveEntity(id_)
            elif type_ == 'give':
                event = event_base.Give(id_)
                _setup_transfer(event, obj)
            elif type_ == 'take':
                event = event_base.Take(id_)
                _setup_transfer(event, obj)
            elif type_ == 'end_game':
                event = event_base.EndGame(id_)
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
                _setup_interaction(event, obj)
            else:
                raise exceptions.InvalidParameterError(
                    "Error: invalid obj of type " + str(type_))

            _setup_event(event, obj)
            return event

        except KeyError as err:
            raise exceptions.InvalidParameterError(
                "Error: JSON is not complete: " + str(err))


def _setup_event(event, obj):
    event.only_once = num_to_bool(obj['once'])
    if 'message' in obj:
        message = obj['message'].strip()
        if message != '':
            event.message = obj['message']


def _setup_transfer(event, obj):
    event.item_id = obj['item']['id']


def _setup_interaction(event, obj):
    event.break_out = obj['breakout']


def make_condition(cond_json, world=None):
    """Creates a new condition.

    Args:
        cond_json (dict): The json blueprint for the condition.
        world (World): The world that is being constructed.

    Return:
        Condition: The newly created condition.
    """
    try:
        type_ = cond_json['type']
        if type_ == 'hasItem':
            return conditions.HasItem(cond_json['item']['id'],
                                      other_json=cond_json['other'], world=world)
        if type_ == 'question':
            return conditions.Question(
                cond_json['question'], cond_json['answer'])
        if type_ == 'protected':
            return conditions.Protected(cond_json['effects'])
        if type_ == 'is_active':
            id_ = cond_json['item']['id']
            entity = world.entities[id_]
            return conditions.IsActive(entity)

        raise exceptions.InvalidParameterError(
            "Condition Factory Error: Invalid object of type " + str(type_))

    except KeyError as err:
        raise exceptions.InvalidParameterError(
            "Error: JSON is not complete: " + str(err))


def num_to_bool(num):
    """Turn a number into a bool."""
    return num != 0
