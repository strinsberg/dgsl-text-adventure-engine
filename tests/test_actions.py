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


# Actions ##############################################################

class TestNullAction(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.action = actions.NullAction(None)

    def test_take_action(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, "Nothing happens")

    def test_execute_event(self):
        self.entity.events.has_event.return_value = True
        self.entity.events.execute.return_value = "Event executed"

        result = self.action._execute_event('use', self.entity)
        self.entity.events.has_event.assert_called_with('use')
        self.entity.events.execute.assert_called_with('use', None)
        self.assertEqual(result, 'Event executed')

    def test_execute_event_no_event(self):
        self.entity.events.has_event.return_value = False

        result = self.action._execute_event('use', self.entity)
        self.entity.events.has_event.assert_called_with('use')
        self.assertIsNone(result)

    def test_filter_entities(self):
        entities = [self.entity]
        result = self.action.filter_entities(entities)
        self.assertIs(result, entities)


# Transfer Actions #####################################################

class TestGo(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.entity.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.action = actions.Go(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, "Go Where?")

    def test_not_active(self):
        self.entity.states.active = False
        result = self.action.take_action(self.entity, self.player)
        self.assertEqual(result, "For some reason you can't")

    def test_has_event(self):
        self.entity.events.has_event.return_value = True
        result = self.action.take_action(self.entity, None)
        self.entity.events.has_event.assert_called_with('go')
        self.entity.events.execute.assert_called_with('go', self.player)
        self.assertEqual(result, "Event executed")

    def test_no_event(self):
        self.entity.events.has_event.return_value = False
        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "Impossible!")


class TestGet(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.entity.spec.name = 'a hat'
        self.entity.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.player.inventory.has_item.return_value = False
        self.action = actions.Get(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, "Get What?")

    def test_already_have(self):
        self.player.inventory.has_item.return_value = True
        result = self.action.take_action(self.entity, None)
        self.player.inventory.has_item.assert_called_with(self.entity.spec.id)
        self.assertEqual(result, "You already have it!")

    @mock.patch('dgsl_engine.actions.move')
    def test_obtainable(self, mock_move):
        self.entity.states.obtainable = True
        self.entity.events.has_event.return_value = True
        self.entity.events.execute.return_value = "Event executed"

        result = self.action.take_action(self.entity, None)
        mock_move.assert_called_with(self.entity, self.player)
        self.assertEqual(result, "You take a hat\nEvent executed")

    def test_obtainable_no_event(self):
        self.entity.states.obtainable = True
        self.entity.events.has_event.return_value = False
        self.entity.events.execute.return_value = "Event executed"

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You take a hat")

    def test_get_not_obtainable(self):
        self.entity.states.obtainable = False

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You can't take that")

    def test_get_filter_entities_only_one(self):
        entities = [self.entity]
        result = self.action.filter_entities(entities)
        self.assertIs(result, entities)

    def test_get_filter_entities_filter_some(self):
        self.player.get.return_value = None
        entities = [self.entity, self.player]
        result = self.action.filter_entities(entities)
        self.assertTrue(len(result) == 1)
        self.assertIs(result[0], self.entity)

    def test_get_filter_entities_filter_some_player_has(self):
        self.player.get.return_value = self.entity
        entities = [self.entity, self.player]
        result = self.action.filter_entities(entities)
        self.assertFalse(result)


class TestDrop(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.entity.spec.name = 'a hat'
        self.entity.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.player.inventory.has_item.return_value = False
        self.action = actions.Drop(self.player)

    def test_use_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, 'Drop What?')

    @mock.patch('dgsl_engine.actions.move')
    def test_drop_player_has_item(self, mock_move):
        self.player.inventory.has_item.return_value = True
        self.entity.events.has_event.return_value = True

        result = self.action.take_action(self.entity, None)
        self.player.inventory.has_item.assert_called_with(self.entity.spec.id)
        mock_move.assert_called_with(self.entity, self.player.owner)
        self.assertEqual(result, "You drop a hat\nEvent executed")

    def test_drop_player_has_item_no_result(self):
        self.player.inventory.has_item.return_value = True
        self.entity.events.has_event.return_value = True
        self.entity.events.execute.return_value = None

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You drop a hat")

    def test_drop_no_item(self):
        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You don't have that")


# Interaction Actions ##################################################

class TestUse(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.entity.spec.name = 'a hat'
        self.entity.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.player.inventory.has_item.return_value = False
        self.action = actions.Use(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, 'Use What?')

    def test_not_active(self):
        self.entity.states.active = False
        result = self.action.take_action(self.entity, self.player)
        self.assertEqual(result, "For some reason you can't")

    def test_has_event(self):
        self.entity.events.has_event.return_value = True

        result = self.action.take_action(self.entity, None)
        self.entity.events.has_event.assert_called_with('use')
        self.entity.events.execute.assert_called_with('use', self.player)
        self.assertEqual(result, "Event executed")

    def test_has_event_no_result(self):
        self.entity.events.has_event.return_value = True
        self.entity.events.execute.return_value = '  '

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You use a hat")

    def test_no_event(self):
        self.entity.events.has_event.return_value = False

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You can't use that")


class TestLook(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.entity.describe.return_value = 'a very nice hat'
        self.entity.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.player.owner.describe.return_value = "A very large room"
        self.action = actions.Look(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, 'A very large room')

    def test_has_event(self):
        self.entity.events.has_event.return_value = True

        result = self.action.take_action(self.entity, None)
        self.entity.events.has_event.assert_called_with('look')
        self.entity.events.execute.assert_called_with('look', self.player)
        self.assertEqual(result, "You see a very nice hat\nEvent executed")

    def test_has_event_no_result(self):
        self.entity.events.has_event.return_value = True
        self.entity.events.execute.return_value = None

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You see a very nice hat")


class TestTalk(unittest.TestCase):
    def setUp(self):
        self.npc = mock.MagicMock()
        self.npc.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.action = actions.Talk(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, 'To Whom?')

    def test_not_active(self):
        self.npc.states.active = False
        result = self.action.take_action(self.npc, self.player)
        self.assertEqual(result, "They don't have anything to say right now")

    def test_has_event(self):
        self.npc.events.has_event.return_value = True
        self.npc.events.execute.return_value = "Hello there!"

        result = self.action.take_action(self.npc, None)
        self.npc.events.has_event.assert_called_with('talk')
        self.npc.events.execute.assert_called_with('talk', self.player)
        self.assertEqual(result, "Hello there!")

    def test_has_event_no_result(self):
        self.npc.events.execute.return_value = None

        result = self.action.take_action(self.npc, None)
        self.assertEqual(result, "That doesn't talk")


# Equipment Actions ####################################################

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.entity = mock.MagicMock()
        self.entity.spec.name = 'a silver ring'
        self.equipment = mock.MagicMock(slot='head')
        self.equipment.spec.name = 'a really big hat'
        self.player = mock.MagicMock()
        self.action = actions.CheckInventory(self.player)

    def test_have_item(self):
        self.player.inventory.has_item.return_value = True

        result = self.action.take_action(self.entity, None)
        self.player.inventory.has_item.assert_called_with(
            self.entity.spec.id)
        self.assertEqual(result, "You have that")

    def test_have_item_equipped(self):
        self.player.inventory.has_item.return_value = False
        self.player.equipped.wearing.return_value = True

        result = self.action.take_action(self.equipment, None)
        self.player.inventory.has_item.assert_called_with(
            self.equipment.spec.id)
        self.player.equipped.wearing.assert_called_with(self.equipment)
        self.assertEqual(result, 'You are wearing that')

    def test_dont_have_it(self):
        self.player.inventory.has_item.return_value = False
        self.player.equipped.wearing.return_value = False

        result = self.action.take_action(self.entity, None)
        self.assertEqual(result, "You don't have that")

    def test_check_inventory(self):
        self.player.inventory.items = [self.entity]
        self.player.equipped.equipment = [self.equipment]

        result = self.action.take_action(None, None)
        self.assertEqual(result, ("You are carrying ...\na silver ring\n\n"
                                  "You are wearing ...\na really big hat"))

    def test_check_inventory_nothing(self):
        self.player.inventory.items = []
        self.player.equipped.equipment = []

        result = self.action.take_action(None, None)
        self.assertEqual(result, ("You are carrying ...\nNothing\n\n"
                                  "You are wearing ...\nNothing"))


class TestEquip(unittest.TestCase):
    def setUp(self):
        self.equipment = mock.MagicMock(slot='head')
        self.equipment.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.equipment.owner = self.player
        self.action = actions.Equip(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, 'Equip What?')

    def test_equip(self):
        self.equipment.events.has_event.return_value = True
        self.equipment.events.execute.return_value = "Executed event"

        result = self.action.take_action(self.equipment, None)
        self.player.equipped.equip.assert_called_with(self.equipment)
        self.player.inventory.remove.assert_called_with(self.equipment.spec.id)
        self.equipment.events.has_event.assert_called_with('equip')
        self.equipment.events.execute.assert_called_with('equip', self.player)
        self.assertEqual(result, "You equip it\nExecuted event")

    def test_equip_no_result(self):
        self.equipment.events.has_event.return_value = True
        self.equipment.events.execute.return_value = ''

        result = self.action.take_action(self.equipment, None)
        self.assertEqual(result, "You equip it")

    def test_equip_no_event(self):
        self.equipment.events.has_event.return_value = False

        result = self.action.take_action(self.equipment, None)
        self.equipment.events.execute.assert_not_called()
        self.assertEqual(result, "You equip it")

    def test_equip_not_equipment(self):
        self.player.equipped.equip.side_effect = AttributeError('foo')

        result = self.action.take_action(self.equipment, None)
        self.player.inventory.remove.assert_not_called()
        self.assertEqual(result, "You can't equip that!")


class TestRemove(unittest.TestCase):
    def setUp(self):
        self.equipment = mock.MagicMock(slot='head')
        self.equipment.events.execute.return_value = "Event executed"
        self.player = mock.MagicMock()
        self.action = actions.Remove(self.player)

    def test_no_entity(self):
        result = self.action.take_action(None, None)
        self.assertEqual(result, 'Remove What?')

    def test_equipped(self):
        self.player.equipped.wearing.return_value = self.equipment.slot
        self.player.equipped.remove.return_value = self.equipment
        self.equipment.events.has_event.return_value = True
        self.equipment.events.execute.return_value = "Executed event"

        result = self.action.take_action(self.equipment, None)
        self.player.equipped.wearing.assert_called_with(self.equipment)
        self.player.equipped.remove.assert_called_with(self.equipment.slot)
        self.player.add.assert_called_with(self.equipment)
        self.equipment.events.has_event.assert_called_with('remove')
        self.equipment.events.execute.assert_called_with('remove', self.player)
        self.assertEqual(result, 'You remove it\nExecuted event')

    def test_equipped_no_result(self):
        self.player.equipped.wearing.return_value = self.equipment.slot
        self.player.equipped.remove.return_value = self.equipment
        self.equipment.events.has_event.return_value = True
        self.equipment.events.execute.return_value = ''

        result = self.action.take_action(self.equipment, None)
        self.assertEqual(result, 'You remove it')

    def test_equipped_no_event(self):
        self.player.equipped.wearing.return_value = self.equipment.slot
        self.player.equipped.remove.return_value = self.equipment
        self.equipment.events.has_event.return_value = False

        result = self.action.take_action(self.equipment, None)
        self.equipment.events.execute.assert_not_called()
        self.assertEqual(result, 'You remove it')

    def test_not_equipped(self):
        self.player.equipped.wearing.return_value = None

        result = self.action.take_action(self.equipment, None)
        self.assertEqual(result, 'You are not wearing that!')


# Not properly implemented #############################################

class TestPlace(unittest.TestCase):
    def test_for_now(self):
        self.action = actions.Place(None)
        self.assertEqual(self.action.take_action(None, None),
                         "Sorry, that action is not available yet.")


# Action Factory #######################################################

class TestActionFactory(unittest.TestCase):
    def setUp(self):
        self.fact = actions.ActionFactory()

    def test_drop(self):
        result = self.fact.new('drop', None)
        self.assertIsInstance(result, actions.Drop)

    def test_get(self):
        result = self.fact.new('get', None)
        self.assertIsInstance(result, actions.Get)

    def test_inventory(self):
        result = self.fact.new('inventory', None)
        self.assertIsInstance(result, actions.CheckInventory)

    def test_look(self):
        result = self.fact.new('look', None)
        self.assertIsInstance(result, actions.Look)

    def test_talk(self):
        result = self.fact.new('talk', None)
        self.assertIsInstance(result, actions.Talk)

    def test_use(self):
        result = self.fact.new('use', None)
        self.assertIsInstance(result, actions.Use)

    def test_equip(self):
        result = self.fact.new('equip', None)
        self.assertIsInstance(result, actions.Equip)

    def test_remove(self):
        result = self.fact.new('remove', None)
        self.assertIsInstance(result, actions.Remove)

    def test_go(self):
        result = self.fact.new('go', None)
        self.assertIsInstance(result, actions.Go)

    def test_place(self):
        result = self.fact.new('give', None)
        self.assertIsInstance(result, actions.Place)

    def test_not_an_action(self):
        result = self.fact.new('bad', None)
        self.assertIsInstance(result, actions.NullAction)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
