import copy


def _extend(obj, extra):
    d = copy.deepcopy(obj)
    d.update(extra)
    return d


# Simple Events ########################################################

EVENT = {
    'id': 'rmr22',
    'once': 0,
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

TAKE = _extend(
    EVENT, {
        'id': 'faeim302',
        'name': 'test take',
        'message': 'Ive been looking for that',
        'type': 'take',
        'item_id': 'none',
    })

TOGGLE_ACTIVE = _extend(
    EVENT, {
        'type': 'toggle_active',
    }
)

TOGGLE_OBTAINABLE = _extend(
    EVENT, {
        'type': 'toggle_obtainable',
    }
)

TOGGLE_HIDDEN = _extend(
    EVENT, {
        'type': 'toggle_hidden',
    }
)

GROUP = _extend(
    EVENT, {
        'type': 'group',
    }
)


ORDERED = _extend(
    EVENT, {
        'type': 'ordered',
    }
)

CONDITIONAL = _extend(
    EVENT, {
        'type': 'conditional',
    }
)

INTERACTION = _extend(
    EVENT, {
        'type': 'interaction',
        'breakout': 0,
    }
)
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
    'items': {}
})

CONTAINER = _extend(OBJ, {
    'id': 'sjaf90fj',
    'type': 'container',
    'name': 'test container',
})

NPC = _extend(OBJ, {
    'id': 'jsd0f',
    'type': 'npc',
    'name': 'pauline',
    'items': {}
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
            },
            {
                'id': NPC['id']
            }
        ]
    })

EQUIPMENT = _extend(
    OBJ, {
        'id': 'fje93jjf',
        'type': 'equipment',
        'name': 'hat',
        'description': 'a red toque with a small stoplight stitched onto the front',
        'slot': 'head',
        'protects': ['cold', 'wind'],
        'must_equip': 1,
    }
)


EQUIPMENT2 = _extend(
    OBJ, {
        'id': 'fan309bk',
        'type': 'equipment',
        'name': 'cap',
        'description': 'a tattered old basebal cap',
        'slot': 'head',
        'protects': ['sun'],
        'must_equip': 1,
    }
)

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

GIVE = _extend(
    EVENT, {
        'id': 'faeim302',
        'name': 'test give',
        'message': 'I bet you will like this!',
        'type': 'give',
        'item_id': 'none',
        'item_owner': {'id': NPC['id']}
    })

# Conditions ###########################################################

HAS_ITEM = {
    'type': 'has_item',
    'item_id': 'm3wsf0dm',
}

QUESTION = {
    'type': 'question',
    'question': 'What is your favorite color?',
    'answer': "I don't know"
}

PROTECTED = {
    'type': 'protected',
    'effects': ['cold', 'wind', 'radiation']
}
