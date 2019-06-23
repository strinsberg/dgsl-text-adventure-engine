import unittest
import dgsl_engine.actions as actions
import dgsl_engine.entity_factory as ent_fact
import dgsl_engine.event_factory as evt_fact
import copy

# I eventually need to move all custom contants and mock to their own modules
# so that they can be reused in each testing environment if possible

# Constant Objects #####################################################

OBJ = {
    'description': 'a simple testing object',
    'active': 1,
    'obtainable': 1,
    'hidden': 0
}


def extend(obj, extra):
    d = copy.deepcopy(obj)
    d.update(extra)
    return d


PLAYER = extend(OBJ, {
    'id': '1234',
    'type': 'player',
    'name': 'test player',
})

ROOM = extend(OBJ, {
    'id': '9234',
    'type': 'room',
    'name': 'test room',
})

CONTAINER = extend(OBJ, {
    'id': 'sjaf90fj',
    'type': 'container',
    'name': 'test container',
})

ENTITY = extend(OBJ, {'id': '23u4', 'type': 'entity', 'name': 'test entity'})

EVENT = {
    'id': 'mf90ae',
    'type': 'event',
    'once': 1,
    'message': "Get it while it's hot",
}

# Mocks ################################################################


class MockCollectorFactory:
    def __init__(self, n):
        self.n = n

    def make(self, *args):
        return self

    def collect(self):
        return [x for x in range(self.n)]


class MockMenuFactory:
    def __init__(self, n):
        self.n = n

    def make(self, *args):
        return self

    def ask(self, *args):
        return self.n


class MockActionFactory:
    def new(self, verb, player, entity, other):
        self.entity = entity
        return self

    def take_action(self):
        if self.entity is None:
            return "Verb with no object"
        return "Result found"


# Tests ################################################################


class TestActionResolver(unittest.TestCase):
    def setUp(self):
        self.col_fact = MockCollectorFactory(0)
        self.menu_fact = MockMenuFactory(0)
        self.act_fact = MockActionFactory()

        self.ent_fact = ent_fact.EntityFactory()
        self.player = self.ent_fact.new(PLAYER)
        self.player.owner = None

        self.parsed_input = {
            'verb': 'unused',
            'object': 'test object',
            'other': None
        }

    def test_resolve_input_verb_only(self):
        resolver = actions.ActionResolver(self.col_fact, self.menu_fact,
                                          self.act_fact)
        self.parsed_input['object'] = '   '
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Verb with no object")

    def test_resolve_input_no_results(self):
        resolver = actions.ActionResolver(self.col_fact, self.menu_fact,
                                          self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "There is no test object")

    def test_resolve_input_one_result(self):
        fact = MockCollectorFactory(1)
        resolver = actions.ActionResolver(fact, self.menu_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Result found")

    def test_resolve_input_many_results(self):
        fact = MockCollectorFactory(5)
        resolver = actions.ActionResolver(fact, self.menu_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Result found")

    def test_resolve_input_many_results_cancel(self):
        fact = MockCollectorFactory(5)
        m_fact = MockMenuFactory(5)
        resolver = actions.ActionResolver(fact, m_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Cancelled")

    def test_resolve_input_many_results_menu_out_of_range(self):
        fact = MockCollectorFactory(5)
        m_fact = MockMenuFactory(-1)
        resolver = actions.ActionResolver(fact, m_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "That is not a choice")


# As each action grows in complexity split this up. The factory can just be
# tested as part of the Actions unless it gets more functionality.
class TestActions(unittest.TestCase):
    def setUp(self):
        self.action_factory = actions.ActionFactory()
        self.ent_fact = ent_fact.EntityFactory()
        self.player = self.ent_fact.new(PLAYER)
        self.room = self.ent_fact.new(ROOM)
        self.container = self.ent_fact.new(CONTAINER)
        self.entity = self.ent_fact.new(ENTITY)
        self.event = evt_fact.EventFactory().new(EVENT)

    def test_null_entity(self):
        action = self.action_factory.new("any", None, None, None)
        self.assertEqual(action.take_action(), "Nothing happens")

    def test_get_from_room(self):
        self.room.add(self.entity)
        action = self.action_factory.new('get', self.player, self.entity, None)
        self.assertEqual(action.take_action(), 'You take test entity')

    def test_get_not_obtainable(self):
        self.entity.states.obtainable = False
        self.room.add(self.entity)
        action = self.action_factory.new('get', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "You can't take that")

    def test_use_has_event(self):
        self.entity.events.add('use', self.event)
        self.room.add(self.entity)
        action = self.action_factory.new('use', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "You use test entity")

    def test_use_no_event(self):
        self.room.add(self.entity)
        action = self.action_factory.new('use', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "You can't use that")


# Main #################################################################

if __name__ == '__main__':
    unittest.main()