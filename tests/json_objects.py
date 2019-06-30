import copy


def _extend(obj, extra):
    d = copy.deepcopy(obj)
    d.update(extra)
    return d


# Simple Events ########################################################

EVENT = {
    'id': 'rmr22',
    'once': 1,
    'type': 'event',
    'name': 'test event',
    'subjects': [],
}

INFORM = _extend(
    EVENT, {
        'id': 'mf90ae',
        'name': 'test event with message',
        'message': "Get it while it's hot",
        'subjects': [{
            'id': EVENT['id']
        }]
    })

GIVE = _extend(
    EVENT, {
        'id': 'faeim302',
        'name': 'test give',
        'message': 'I bet you will like this!',
        'type': 'give'
    })

TAKE = _extend(
    EVENT, {
        'id': 'faeim302',
        'name': 'test take',
        'message': 'Ive been looking for that',
        'type': 'take'
    })

# Entities #############################################################

OBJ = {
    'description': 'a simple testing object',
    'active': 1,
    'obtainable': 1,
    'hidden': 0,
    'events': [{
        'id': INFORM['id'],
        'verb': 'use',
    }]
}

ENTITY = _extend(OBJ, {'id': '23u4', 'type': 'entity', 'name': 'test entity'})

PLAYER = _extend(OBJ, {
    'id': '1234',
    'type': 'player',
    'name': 'test player',
})

CONTAINER = _extend(OBJ, {
    'id': 'sjaf90fj',
    'type': 'container',
    'name': 'test container',
})

ROOM = _extend(
    OBJ, {
        'id': '9234',
        'type': 'room',
        'name': 'test room',
        'description': 'You are in a strange test room',
        'items': [
            {
                'id': PLAYER['id'],
            },
            {
                'id': ENTITY['id']
            },
            {
                'id': CONTAINER['id']
            }
        ]
    })

# Events that need Entities ############################################

MOVE = _extend(
    EVENT, {
        'id': 'ru490',
        'type': 'move',
        'name': 'test move event',
        'destination': {
            'id': ROOM['id']
        },
        'verb': 'use',
        'subjects': [
            {
                'id': INFORM['id']
            }
        ]
    })
