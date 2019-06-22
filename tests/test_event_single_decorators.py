import unittest
import dgsl_engine.event_single_decorators as decorators
import dgsl_engine.event_base as event_base

ID = "m3f208"
MESSAGE = "It's been a long time old friend"
NOTE = "You shouldn't trust this person!"

# Mocks ################################################################


class MockVisitor:
    def visit_event(self, event):
        self.result = event.id


# Tests ################################################################


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.base_with_message = decorators.MessageDecorator(
            event_base.Event(ID), MESSAGE)

    def test_decorator_has_event_id(self):
        self.assertEqual(self.base_with_message.id, ID)

    def test_message_with_base_only(self):
        self.assertEqual(self.base_with_message.execute(None), MESSAGE)

    def test_message_with_more(self):
        message = decorators.MessageDecorator(self.base_with_message, NOTE)
        self.assertEqual(message.execute(None), MESSAGE + '\n' + NOTE)

    def test_visit(self):
        visitor = MockVisitor()
        self.base_with_message.accept(visitor)
        self.assertEqual(visitor.result, ID)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()