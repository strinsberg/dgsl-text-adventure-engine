def take_action(parsed_command, world):
    subject = parsed_command['subject']
    verb = parsed_command['verb']
    if verb == 'get':
        message = _get(world.player, subject)
    elif verb == 'use':
        message = _use(world.player, subject)

    if subject.events.has_event(verb):
        print(subject.events.execute(verb, subject))
        message += "\n" + subject.events.execute(verb, subject)
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