import unittest
import dgsl_engine.interaction as interaction
from dgsl_engine.event_factory import EventFactory
from . import json_objects as objects
from . import fakes


class TestInteraction(unittest.TestCase):
    def setUp(self):
        pass

    def test_execute(self):
        pass


class TestOption(unittest.TestCase):
    def setUp(self):
        self.fact = EventFactory()
        self.event = self.fact.new(objects.INFORM)
        self.option = interaction.Option('Ask for advice', self.event)

    def test_is_visible(self):
        vis = self.option.is_visible(None)
        self.assertTrue(vis)

    def test_is_visible_false(self):
        self.event.is_done = True
        vis = self.option.is_visible(None)
        self.assertFalse(vis)

    def test_choose(self):
        result = self.option.choose(None)
        self.assertEqual(result, "Get it while it's hot")


class TestConditionalOption(unittest.TestCase):
    def setUp(self):
        self.fact = EventFactory()
        self.event = self.fact.new(objects.INFORM)
        self.will_pass = fakes.FakeCondition(True)
        self.will_fail = fakes.FakeCondition(False)
        self.option = interaction.ConditionalOption(
            'Ask for advice', self.event, self.will_pass)

    def test_is_visible(self):
        vis = self.option.is_visible(None)
        self.assertTrue(vis)

    def test_is_visible_false(self):
        option = interaction.ConditionalOption(
            'Ask for advice', self.event, self.will_fail)
        vis = option.is_visible(None)
        self.assertFalse(vis)

    def test_is_visible_is_done(self):
        self.event.is_done = True
        vis = self.option.is_visible(None)
        self.assertFalse(vis)
