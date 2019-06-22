import unittest
import dgsl_engine.entity_base as entity

ID = "1234"
ID2 = "5678"
NULL = "Null"
VERB = "look"
VERB2 = "use"

# Mocks ###############################################################


class MockEvent:
    def execute(self, entity):
        return entity.describe()


class MockVisitor:
    def visit_entity(self, entity):
        self.result = entity.spec.id


# Entity tests ########################################################


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.entity = entity.Entity(ID)

    def test_init(self):
        self.assertEqual(self.entity.spec.id, ID)
        self.assertEqual(self.entity.spec.name, NULL)
        self.assertEqual(self.entity.states.active, True)
        self.assertFalse(self.entity.events.events)

    def test_describe(self):
        description = "A nice entity"
        self.entity.spec.description = description
        self.assertEqual(self.entity.describe(), description)

    def test_visit(self):
        visitor = MockVisitor()
        self.entity.accept(visitor)
        self.assertEqual(visitor.result, ID)


# Supporting classes ##################################################


class TestSpec(unittest.TestCase):
    def setUp(self):
        self.spec = entity.EntitySpec(ID)

    def test_init(self):
        self.assertEqual(self.spec.id, ID)
        self.assertEqual(self.spec.name, NULL)
        self.assertEqual(self.spec.description, NULL)


class TestStates(unittest.TestCase):
    def test_init(self):
        states = entity.EntityStates()
        self.assertTrue(states.active)
        self.assertTrue(states.obtainable)
        self.assertFalse(states.hidden)


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.mock_event = MockEvent()
        self.other_mock_event = MockEvent()
        self.events = entity.EntityEvents()
        self.entity = entity.Entity(ID)
        self.events.add(VERB, self.mock_event)

    def test_add_new(self):
        self.assertTrue(self.events.add(VERB2, self.other_mock_event))
        self.assertTrue(VERB2 in self.events.events)

    def test_add_already_there(self):
        self.assertFalse(self.events.add(VERB, self.mock_event))

    def test_has(self):
        self.events.add(VERB, self.mock_event)
        self.assertTrue(self.events.has_event(VERB))

    def test_execute(self):
        self.events.add(VERB, self.mock_event)
        self.assertEqual(self.events.execute(VERB, self.entity), NULL)


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


# Main #################################################################s

if __name__ == '__main__':
    unittest.main()
