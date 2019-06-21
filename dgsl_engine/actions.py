def take_action(verb, obj, other, world):
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