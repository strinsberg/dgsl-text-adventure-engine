from . import user_input


class ActionResolver:
    def __init__(self, collector_factory):
        self.collector_fact = collector_factory

    def resolve_input(self, parsed_input, world):
        if parsed_input['code'] is not None:
            return parsed_input['message']

        entities = self.collector_fact.make(parsed_input['object'],
                                            parsed_input['other'],
                                            world.player.owner)
        size = len(entities)
        if size > 1:
            menu = user_input.Menu(entities)
            idx = menu.ask()
            if idx != size:
                entity = entities[idx]
            else:
                return "Cancelled"

        if size == 1:
            entity = entities[0]
        elif size == 0:
            pass

        # Eventually add the other collecting code
        return _take_action(parsed_input['verb'], entity, None, world)


def _take_action(verb, obj, other, world):
    # will eventually have to deal with other. Might just pass it to the action.
    if verb == 'get':
        message = _get(world.player, obj)
    elif verb == 'use':
        message = _use(world.player, obj)

    if obj.events.has_event(verb):
        print(obj.events.execute(verb, obj))
        message += "\n" + obj.events.execute(verb, obj)
    return message


def move(entity, destination):
    here = entity.owner
    if destination.add(entity):
        here.inventory.remove(entity.spec.id)


def _get(player, entity):
    if entity.states.obtainable:
        move(entity, player)
        return "You take " + entity.spec.name
    return "You can't take that"


def _use(player, entity):
    if entity.events.has_event('use'):
        return "You use " + entity.spec.name
    return "You can't use that"