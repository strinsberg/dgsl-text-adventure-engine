import unittest
import dgsl_engine.actions as actions
import dgsl_engine.entity_factory as ent_fact
import dgsl_engine.event_factory as evt_fact
from . import json_objects as objects
from . import fakes

# Tests ################################################################


class TestActionResolver(unittest.TestCase):
    def setUp(self):
        self.col_fact = fakes.FakeCollector(0)
        self.menu_fact = fakes.FakeMenu(0)
        self.act_fact = fakes.FakeAction()

        self.ent_fact = ent_fact.EntityFactory()
        self.player = self.ent_fact.new(objects.PLAYER)
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
        fact = fakes.FakeCollector(1)
        resolver = actions.ActionResolver(fact, self.menu_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Result found")

    def test_resolve_input_many_results(self):
        fact = fakes.FakeCollector(5)
        resolver = actions.ActionResolver(fact, self.menu_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Result found")

    def test_resolve_input_many_results_cancel(self):
        fact = fakes.FakeCollector(5)
        m_fact = fakes.FakeMenu(5)
        resolver = actions.ActionResolver(fact, m_fact, self.act_fact)
        self.assertEqual(
            resolver.resolve_input(self.parsed_input, self.player),
            "Cancelled")

    def test_resolve_input_many_results_menu_out_of_range(self):
        fact = fakes.FakeCollector(5)
        m_fact = fakes.FakeMenu(-1)
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
        self.player = self.ent_fact.new(objects.PLAYER)
        self.room = self.ent_fact.new(objects.ROOM)
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.event = evt_fact.EventFactory().new(objects.INFORM)

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
        self.assertEqual(action.take_action(),
                         "You use test entity\nGet it while it's hot")

    def test_use_no_event(self):
        self.room.add(self.entity)
        action = self.action_factory.new('use', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "You can't use that")


# Main #################################################################

if __name__ == '__main__':
    unittest.main()