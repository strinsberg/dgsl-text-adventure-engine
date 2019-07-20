import unittest
from dgsl_engine.event_factory import EventFactory
import dgsl_engine.exceptions as exceptions
from . import json_objects as objects
from . import fakes


# Tests ################################################################

class TestGroupEvent(unittest.TestCase):
    def setUp(self):
        self.fact = EventFactory()
        self.group = self.fact.new(objects.GROUP)
        self.inform = self.fact.new(objects.INFORM)
        self.event = self.fact.new(objects.EVENT)
        self.group.add(self.event)
        self.group.add(self.inform)

    def test_add(self):
        self.assertIn(self.inform, self.group.events)

    def test_add_raises(self):
        with self.assertRaises(exceptions.InvalidParameterError):
            self.group.add(self.event)

    def test_execute(self):
        res = self.group.execute(None)
        self.assertEqual(res, "Get it while it's hot")

    def test_execute_has_message(self):
        self.group.message = 'What just happend?'
        res = self.group.execute(None)
        self.assertEqual(res, "What just happend?\nGet it while it's hot")

    def test_accept(self):
        visitor = fakes.FakeEventVisitor()
        self.group.accept(visitor)
        self.assertEqual(visitor.result, self.group.id)


class TestOrderedGroup(unittest.TestCase):
    def setUp(self):
        self.fact = EventFactory()
        self.ordered = self.fact.new(objects.ORDERED)
        self.inform = self.fact.new(objects.INFORM)
        self.event = self.fact.new(objects.EVENT)
        self.event.message = 'How dare you!'
        self.ordered.add(self.event)
        self.ordered.add(self.inform)

    def test_add(self):
        self.assertIn(self.inform, self.ordered.events)
        self.assertTrue(self.event.only_once)

    def test_execute(self):
        res = self.ordered.execute(None)
        self.assertEqual(res, 'How dare you!')
        res = self.ordered.execute(None)
        self.assertEqual(res, "Get it while it's hot")
        res = self.ordered.execute(None)
        self.assertEqual(res, "Get it while it's hot")

    def test_execute_has_message(self):
        self.ordered.message = 'Why?'
        res = self.ordered.execute(None)
        self.assertEqual(res, 'Why?\nHow dare you!')
        res = self.ordered.execute(None)
        self.assertEqual(res, "Why?\nGet it while it's hot")

    def test_execute_only_message(self):
        self.ordered.message = 'Stop bothering me!'
        self.inform.message = None
        self.event.message = None
        res = self.ordered.execute(None)
        self.assertEqual(res, 'Stop bothering me!')

    def test_execute_all_only_once(self):
        self.inform.only_once = True
        self.event.only_once = True
        self.ordered.execute(None)
        self.ordered.execute(None)
        res = self.ordered.execute(None)
        self.assertEqual(res, '')


class TestConditionalEvent(unittest.TestCase):
    def setUp(self):
        self.fact = EventFactory()
        self.conditional = self.fact.new(objects.CONDITIONAL)
        self.success = self.fact.new(objects.INFORM)
        self.failure = self.fact.new(objects.EVENT)
        self.failure.message = 'Not a chance!'
        self.will_pass = fakes.FakeCondition(True)
        self.will_fail = fakes.FakeCondition(False)

    def test_execute_success(self):
        self.conditional.condition = self.will_pass
        self.conditional.success = self.success
        res = self.conditional.execute(None)
        self.assertEqual(res, "Get it while it's hot")
        self.assertFalse(self.conditional.is_done)
        res = self.conditional.execute(None)
        self.assertEqual(res, "Get it while it's hot")

    def test_execute_success_only_once(self):
        self.conditional.condition = self.will_pass
        self.conditional.success = self.success
        self.conditional.only_once = True
        res = self.conditional.execute(None)
        self.assertEqual(res, "Get it while it's hot")
        self.assertTrue(self.conditional.is_done)

    def test_execute_failure(self):
        self.conditional.condition = self.will_fail
        self.conditional.failure = self.failure
        res = self.conditional.execute(None)
        self.assertEqual(res, 'Not a chance!')

    def test_execute_fail_no_failure(self):
        self.conditional.condition = self.will_fail
        res = self.conditional.execute(None)
        self.assertEqual(res, '')

    def test_execute_with_message_success(self):
        self.conditional.condition = self.will_pass
        self.conditional.message = 'Come back anytime!'
        self.conditional.success = self.success
        res = self.conditional.execute(None)
        self.assertEqual(res, "Come back anytime!\nGet it while it's hot")

    def test_execute_with_message_failure(self):
        self.conditional.condition = self.will_fail
        self.conditional.message = 'Come back anytime!'
        self.conditional.failure = self.failure
        res = self.conditional.execute(None)
        self.assertEqual(res, "Come back anytime!\nNot a chance!")

    def test_execute_only_message(self):
        self.conditional.condition = self.will_pass
        self.conditional.message = 'Come back anytime!'
        self.conditional.success = self.success
        self.success.message = ''
        res = self.conditional.execute(None)
        self.assertEqual(res, "Come back anytime!")

    def test_accept(self):
        visitor = fakes.FakeEventVisitor()
        self.conditional.accept(visitor)
        self.assertEqual(visitor.result, self.conditional.id)


# Main #################################################################
if __name__ == '__main__':
    unittest.main()
