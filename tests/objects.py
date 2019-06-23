import copy


def _extend(obj, extra):
    d = copy.deepcopy(obj)
    d.update(extra)
    return d


OBJ = {
    'description': 'a simple testing object',
    'active': 1,
    'obtainable': 1,
    'hidden': 0
}

PLAYER = _extend(OBJ, {
    'id': '1234',
    'type': 'player',
    'name': 'test player',
})

ROOM = _extend(OBJ, {
    'id': '9234',
    'type': 'room',
    'name': 'test room',
})

CONTAINER = _extend(OBJ, {
    'id': 'sjaf90fj',
    'type': 'container',
    'name': 'test container',
})

ENTITY = _extend(OBJ, {'id': '23u4', 'type': 'entity', 'name': 'test entity'})

INFORM = {
    'id': 'mf90ae',
    'type': 'event',
    'once': 1,
    'message': "Get it while it's hot",
}