import unittest
from unittest import mock
import dgsl_engine.actions as actions


# Tests ################################################################

class TestActionResolver(unittest.TestCase):
    def setUp(self):
        self.collector = mock.MagicMock()
        self.col_fact = mock.MagicMock()
        self.col_fact.make.return_value = self.collector

        self.menu = mock.MagicMock()
        self.menu_fact = mock.MagicMock()
        self.menu_fact.make.return_value = self.menu

        self.action = mock.MagicMock()
        self.act_fact = mock.MagicMock()
        self.act_fact.new.return_value = self.action

        self.player = mock.MagicMock()

        self.resolver = actions.ActionResolver(
            self.col_fact, self.menu_fact, self.act_fact)

        self.parsed_input = {
            'verb': 'unused',
            'object': 'test object',
            'other': None
        }

    def test_resolve_input_verb_only(self):
        self.parsed_input['object'] = '   '
        self.action.take_action.return_value = 'Action Taken'
        result = self.resolver.resolve_input(self.parsed_input, self.player)

        self.act_fact.new.assert_called_with(
            self.parsed_input['verb'], self.player)
        self.action.take_action.assert_called_with(None, None)
        self.assertEqual(result, "Action Taken")

    def test_resolve_input_no_results(self):
        self.action.filter_entities.return_value = []
        result = self.resolver.resolve_input(self.parsed_input, self.player)

        self.action.filter_entities.assert_called_with(
            self.collector.collect())
        self.assertEqual(result, "There is no test object")

    def test_resolve_input_one_result(self):
        entity = mock.MagicMock()
        self.action.filter_entities.return_value = [entity]
        self.action.take_action.return_value = "Action Taken"
        result = self.resolver.resolve_input(self.parsed_input, self.player)

        self.action.take_action.assert_called_with(entity, None)
        self.assertEqual(result, "Action Taken")

    def test_resolve_input_many_results(self):
        self.action.take_action.return_value = "Action Taken"
        entity = mock.MagicMock()
        entity.spec.name = 'George'
        other_entity = mock.MagicMock()
        other_entity.spec.name = 'Sally'
        self.action.filter_entities.return_value = [entity, other_entity]
        self.menu.ask.return_value = 1

        result = self.resolver.resolve_input(self.parsed_input, self.player)
        self.menu_fact.make.assert_called_with(['George', 'Sally'])
        self.action.take_action.assert_called_with(other_entity, None)
        self.assertEqual(result, '\nAction Taken')

    def test_resolve_input_many_results_cancel(self):
        entity = mock.MagicMock()
        entity.spec.name = 'George'
        other_entity = mock.MagicMock()
        other_entity.spec.name = 'Sally'
        self.action.filter_entities.return_value = [entity, other_entity]
        self.menu.ask.return_value = 2

        result = self.resolver.resolve_input(self.parsed_input, self.player)
        self.assertEqual(result, '\nCancelled')

    def test_resolve_input_many_results_menu_out_of_range(self):
        entity = mock.MagicMock()
        entity.spec.name = 'George'
        other_entity = mock.MagicMock()
        other_entity.spec.name = 'Sally'
        self.action.filter_entities.return_value = [entity, other_entity]
        self.menu.ask.return_value = -1

        result = self.resolver.resolve_input(self.parsed_input, self.player)
        self.assertEqual(result, '\nThat is not a choice')


# As each action grows in complexity split this up. The factory can just be
# tested as part of the Actions unless it gets more functionality.
@unittest.skip
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
        self.entity.events.add('get', self.event)
        self.room.add(self.entity)
        action = self.action_factory.new('get', self.player, self.entity, None)
        self.assertEqual(action.take_action(),
                         "You take test entity\nGet it while it's hot")

    def test_get_from_room_no_event(self):
        self.room.add(self.entity)
        action = self.action_factory.new('get', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "You take test entity")

    def test_get_no_target_object(self):
        action = self.action_factory.new('get', self.player, None, None)
        self.assertEqual(action.take_action(), "Get what?")

    def test_get_player_has(self):
        self.player.add(self.entity)
        action = self.action_factory.new('get', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "You already have it")

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

    def test_use_no_target(self):
        action = self.action_factory.new('use', self.player, None, None)
        self.assertEqual(action.take_action(), "Use what?")

    def test_drop(self):
        self.room.add(self.player)
        self.player.add(self.entity)
        self.entity.events.add('drop', self.event)
        action = self.action_factory.new('drop', self.player, self.entity,
                                         None)
        self.assertEqual(action.take_action(),
                         "You drop test entity\nGet it while it's hot")

    def test_drop_no_event(self):
        self.room.add(self.player)
        self.player.add(self.entity)
        action = self.action_factory.new('drop', self.player, self.entity,
                                         None)
        self.assertEqual(action.take_action(), 'You drop test entity')

    def test_drop_no_item(self):
        action = self.action_factory.new('drop', self.player, self.entity,
                                         None)
        self.assertEqual(action.take_action(), "You don't have it")

    def test_drop_no_target(self):
        action = self.action_factory.new('drop', self.player, None, None)
        self.assertEqual(action.take_action(), "Drop what?")

    def test_look(self):
        self.room.add(self.player)
        self.entity.events.add('look', self.event)
        action = self.action_factory.new('look', self.player, self.entity,
                                         None)
        self.assertEqual(
            action.take_action(),
            "You see a simple testing object\nGet it while it's hot")

    def test_look_no_event(self):
        self.room.add(self.player)
        action = self.action_factory.new('look', self.player, self.entity,
                                         None)
        self.assertEqual(action.take_action(),
                         "You see a simple testing object")

    def test_look_no_target(self):
        self.room.add(self.player)
        action = self.action_factory.new('look', self.player, None, None)
        self.assertEqual(action.take_action(),
                         "You are in a strange test room")

    def test_check_inventory(self):
        self.player.add(self.entity)
        self.player.add(self.container)
        action = self.action_factory.new('inventory', self.player, None, None)
        self.assertEqual(action.take_action(), ("You are carrying ...\n"
                                                "a simple testing object\n"
                                                "a simple testing object"))

    def test_check_inventory_empty(self):
        action = self.action_factory.new('inventory', self.player, None, None)
        self.assertEqual(action.take_action(), "You are carrying ...\nNothing")

    def test_check_for_item_in_inventory(self):
        self.player.add(self.entity)
        action = self.action_factory.new('inventory', self.player, self.entity,
                                         None)
        self.assertEqual(action.take_action(), "You have that")

    def test_check_for_item_not_there(self):
        action = self.action_factory.new('inventory', self.player, self.entity,
                                         None)
        self.assertEqual(action.take_action(), "You don't have that")

    def test_talk(self):
        action = self.action_factory.new(
            'talk', self.player, self.entity, None)
        self.entity.events.add('talk', self.event)
        self.assertEqual(action.take_action(), "Get it while it's hot")

    def test_talk_doest_talk(self):
        action = self.action_factory.new(
            'talk', self.player, self.entity, None)
        self.assertEqual(action.take_action(), "That doesn't talk")

    def test_talk_no_target(self):
        action = self.action_factory.new(
            'talk', self.player, None, None)
        self.assertEqual(action.take_action(), "To whom?")


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
