import unittest
import dgsl_engine.entity_base as entity

ID = "1234"
NULL = "Null"
VERB = "look"

# Mocks ###############################################################


class MockEvent:
    def __init__(self):
        self.verb = VERB

    def execute(self, entity):
        return entity.describe()


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


# Supporting classes ##################################################


class TestSpec(unittest.TestCase):
    def setUp(self):
        self.spec = entity.Spec(ID)

    def test_init(self):
        self.assertEqual(self.spec.id, ID)
        self.assertEqual(self.spec.name, NULL)
        self.assertEqual(self.spec.description, NULL)

    def test_matches(self):
        spec = entity.Spec(ID)
        self.assertTrue(self.spec.matches(spec))


class TestStates(unittest.TestCase):
    def test_init(self):
        states = entity.States()
        self.assertTrue(states.active)
        self.assertTrue(states.obtainable)
        self.assertFalse(states.hidden)


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.mock_event = MockEvent()
        self.events = entity.Events()
        self.entity = entity.Entity(ID)

    def test_add(self):
        self.events.add(self.mock_event)
        self.assertTrue(VERB in self.events.events)

    def test_has(self):
        self.events.add(self.mock_event)
        self.assertTrue(self.events.has_event(VERB))

    def test_execute(self):
        self.events.add(self.mock_event)
        self.assertEqual(self.events.execute(VERB, self.entity), NULL)


if __name__ == '__main__':
    unittest.main()
