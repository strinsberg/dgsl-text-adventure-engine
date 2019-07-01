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


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
