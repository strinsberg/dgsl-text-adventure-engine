import unittest
from dgsl_engine.event_factory import EventFactory
import dgsl_engine.exceptions as exceptions
from . import json_objects as objects


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
        self.assertEqual(res, "Get it while it's hot\nWhat just happend?")


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
        self.assertEqual(res, 'How dare you!\nWhy?')
        res = self.ordered.execute(None)
        self.assertEqual(res, "Get it while it's hot\nWhy?")

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
        self.assertEqual(res, 'Nothing happens')


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
