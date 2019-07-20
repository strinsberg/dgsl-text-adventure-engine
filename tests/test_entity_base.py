import unittest
import unittest.mock as mock
import dgsl_engine.entity_base as entity

# Constants ############################################################

ID = "1234"
ID2 = "5678"
NULL = "Null"
USE = "use"
LOOK = "look"


# Entity tests #########################################################

class TestEntity(unittest.TestCase):

    def setUp(self):
        self.entity = entity.Entity(ID)

    def test_describe(self):
        description = "A nice entity"
        self.entity.spec.description = description
        self.assertEqual(self.entity.describe(), description)

    def test_visit(self):
        visitor = mock.MagicMock()
        self.entity.accept(visitor)
        self.assertTrue(visitor.visit_entity.assert_called)

    def test_repr(self):
        rep = "<Entity '{}', Name: '{}'>".format(
            self.entity.spec.id, self.entity.spec.name)
        self.assertEqual(repr(self.entity), rep)


# Supporting classes ###################################################


class TestSpec(unittest.TestCase):
    def setUp(self):
        self.spec = entity.EntitySpec(ID)

    def test_init(self):
        self.assertEqual(self.spec.id, ID)
        self.assertEqual(self.spec.name, NULL)
        self.assertEqual(self.spec.description, NULL)


class TestStates(unittest.TestCase):
    def setUp(self):
        self.states = entity.EntityStates()

    def test_toggle_active(self):
        self.assertTrue(self.states.active)
        self.states.toggle_active()
        self.assertFalse(self.states.active)
        self.states.toggle_active()
        self.assertTrue(self.states.active)

    def test_toggle_obtainable(self):
        self.assertTrue(self.states.obtainable)
        self.states.toggle_obtainable()
        self.assertFalse(self.states.obtainable)
        self.states.toggle_obtainable()
        self.assertTrue(self.states.obtainable)

    def test_toggle_hidden(self):
        self.assertFalse(self.states.hidden)
        self.states.toggle_hidden()
        self.assertTrue(self.states.hidden)
        self.states.toggle_hidden()
        self.assertFalse(self.states.hidden)


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.mock_use = mock.MagicMock()
        self.mock_use.execute.return_value = 'You use it'
        self.mock_look = mock.MagicMock()
        self.events = entity.EntityEvents()
        self.events.add(USE, self.mock_use)

    def test_add_new(self):
        self.assertTrue(self.events.add(LOOK, self.mock_look))
        self.assertTrue(self.events.events[LOOK] == self.mock_look)

    def test_add_already_there(self):
        self.assertFalse(self.events.add(USE, self.mock_use))

    def test_has(self):
        self.events.add(USE, self.mock_use)
        self.assertTrue(self.events.has_event(USE))

    def test_execute(self):
        self.events.add(USE, self.mock_use)
        self.assertTrue(self.mock_use.execute.assert_called)
        self.assertEqual(self.events.execute(USE, None), 'You use it')


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = entity.Inventory()
        self.entity = entity.Entity(ID)
        self.entity2 = entity.Entity(ID2)
        self.inventory.add(self.entity)

    def test_add_new(self):
        self.assertTrue(self.inventory.add(self.entity2))
        self.assertTrue(ID2 in self.inventory.items)

    def test_add_already_there(self):
        self.assertFalse(self.inventory.add(self.entity))

    def test_remove(self):
        removed = self.inventory.remove(ID)
        self.assertEqual(self.entity, removed)

    def test_has_item(self):
        self.assertTrue(self.inventory.has_item(ID))

    def test_iter(self):
        self.inventory.add(self.entity2)
        ids = []
        for item in self.inventory:
            ids.append(item.spec.id)
        self.assertEqual(", ".join(ids), ", ".join([ID, ID2]))


class TestEquipped(unittest.TestCase):
    def setUp(self):
        self.mock_hat = mock.MagicMock(slot='head')
        self.equipped = entity.Equipped(None)

    def test_equip(self):
        old = self.equipped.equip(self.mock_hat)
        self.assertIs(self.equipped.equipment['head'], self.mock_hat)
        self.assertIsNone(old)

    def test_equip_already_there(self):
        mock_helmet = mock.MagicMock(slot='head')
        self.equipped.equip(self.mock_hat)
        old = self.equipped.equip(mock_helmet)
        self.assertIs(self.equipped.equipment['head'], mock_helmet)
        self.assertIs(old, self.mock_hat)

    def test_remove(self):
        self.equipped.equip(self.mock_hat)
        ent = self.equipped.remove('head')
        self.assertIs(ent, self.mock_hat)
        self.assertNotIn('head', self.equipped.equipment)

    def test_remove_not_there(self):
        self.assertNotIn('head', self.equipped.equipment)
        ent = self.equipped.remove('head')
        self.assertIsNone(ent)

    def test_get(self):
        self.equipped.equip(self.mock_hat)
        ent = self.equipped.get('head')
        self.assertIs(ent, self.mock_hat)
        self.assertIs(self.equipped.equipment['head'], self.mock_hat)

    def test_get_not_there(self):
        ent = self.equipped.get('head')
        self.assertIsNone(ent, self.mock_hat)

    def test_wearing(self):
        self.mock_hat.spec = mock.MagicMock(name='hat')
        self.equipped.equip(self.mock_hat)
        wearing = self.equipped.wearing(self.mock_hat)
        self.assertIs(wearing, self.mock_hat.slot)

    def test_not_wearing(self):
        self.mock_hat.spec = mock.MagicMock(name='hat')
        wearing = self.equipped.wearing(self.mock_hat)
        self.assertIsNone(wearing)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
