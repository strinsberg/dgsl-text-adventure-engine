import copy


def _extend(obj, extra):
    d = copy.deepcopy(obj)
    d.update(extra)
    return d


# Conditions ###########################################################

HAS_ITEM = {
    'type': 'hasItem',
    'item': {'id': 'm3wsf0dm'},
}

QUESTION = {
    'type': 'question',
    'question': 'What is your favorite color?',
    'answer': "I don't know",
    'id': 'js09fs',
}

PROTECTED = {
    'type': 'protected',
    'effects': ['cold', 'wind', 'radiation']
}


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
        'events': [
            {'id': EVENT['id']},
            {'id': INFORM['id']}
        ]
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
        'condition': {'id': QUESTION['id']},
        'success': {'id': EVENT['id']},
        'failure': {'id': INFORM['id']}
    })

INTERACTION = _extend(
    EVENT, {
        'type': 'interaction',
        'breakout': 0,
        'options': [
            {
                'id': 'sdfjsa',
                'type': 'option',
                'text': 'help out',
                'event': {'id': EVENT['id']}
            },
            {
                'id': 'fjsiajfo',
                'type': 'conditional',
                'text': 'ask about barn swallows',
                'event': {'id': INFORM['id']},
                'condition': {'id': QUESTION},
            }
        ]
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
        'item': {'id': 'none'},
        'item_owner': {'id': NPC['id']}
    })

TAKE = _extend(
    EVENT, {
        'id': 'faeim302',
        'name': 'test take',
        'message': 'Ive been looking for that',
        'type': 'take',
        'item': {'id': 'none'},
        'new_owner': {'id': NPC['id']}
    })

TOGGLE_ACTIVE = _extend(
    EVENT, {
        'type': 'toggle_active',
        'target': {'id': NPC['id']}
    }
)
