import unittest
import dgsl_engine.event_base as event_base
import dgsl_engine.entity_base as entity_base

ID = '1234'
RESULT = ''

# Mocks ################################################################


class MockVisitor:
    def visit_event(self, event):
        self.result = event.id


# Tests ################################################################


class TestEventBase(unittest.TestCase):
    def setUp(self):
        self.event = event_base.Event(ID)
        self.other_event = event_base.Event(ID)
        self.entity = entity_base.Entity(ID)

    def test_init(self):
        self.assertFalse(self.event.is_done)
        self.assertFalse(self.event.only_once)

    def test_execute(self):
        # Will need to change when event gets subjects
        self.assertEqual(self.event.execute(self.entity), RESULT)

    def test_visit(self):
        visitor = MockVisitor()
        self.event.accept(visitor)
        self.assertEqual(visitor.result, ID)

    def test_register(self):
        self.event.register(self.other_event)
        self.assertIn(self.other_event, self.event.subjects)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()