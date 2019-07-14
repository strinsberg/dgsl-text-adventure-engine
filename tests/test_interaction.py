import unittest
import dgsl_engine.interaction as interaction
from dgsl_engine.event_factory import EventFactory
from . import json_objects as objects
from . import fakes


class TestInteraction(unittest.TestCase):
    def setUp(self):
        self.fact = EventFactory()
        self.inform = self.fact.new(objects.INFORM)
        self.event = self.fact.new(objects.EVENT)
        self.event.message = 'I will need help with this'

        self.interaction = self.fact.new(objects.INTERACTION)
        self.option = interaction.Option('Ask for advice', self.inform)
        self.option2 = interaction.Option('Fix the reactor', self.event)
        self.interaction.add(self.option)
        self.interaction.add(self.option2)

    def test_execute_all_visible(self):
        out_ = fakes.FakeOutput()
        in_ = fakes.FakeInput(['1', '2', '3'])
        self.interaction._out = out_.make_capture()
        self.interaction._in = in_.make_stream()
        self.interaction.execute(None)
        self.assertEqual(out_.get_text(),
                         ("\n1. Ask for advice\n"
                          "2. Fix the reactor\n"
                          "3. Cancel\n\n"
                          "--------------------------------------------------\n"
                          "Get it while it's hot\n\n"

                          "1. Ask for advice\n"
                          "2. Fix the reactor\n"
                          "3. Cancel\n\n"
                          "--------------------------------------------------\n"
                          "I will need help with this\n\n"

                          "1. Ask for advice\n"
                          "2. Fix the reactor\n"
                          "3. Cancel\n\n"))

    def test_execute_not_all_visible(self):
        out_ = fakes.FakeOutput()
        in_ = fakes.FakeInput(['2'])
        self.interaction._out = out_.make_capture()
        self.interaction._in = in_.make_stream()
        self.event.is_done = True
        self.interaction.execute(None)
        self.assertEqual(out_.get_text(), "\n1. Ask for advice\n2. Cancel\n\n")

    def test_execute_breakout(self):
        self.interaction.break_out = True
        out_ = fakes.FakeOutput()
        in_ = fakes.FakeInput(['1'])
        self.interaction._out = out_.make_capture()
        self.interaction._in = in_.make_stream()
        self.inform.is_done = True
        self.interaction.execute(None)
        self.assertEqual(out_.get_text(),
                         ("\n1. Fix the reactor\n"
                          "2. Cancel\n\n"
                          "--------------------------------------------------\n"
                          "I will need help with this\n\n"))

    def test_execute_with_message(self):
        self.interaction.message = 'Come again soon!'
        out_ = fakes.FakeOutput()
        in_ = fakes.FakeInput(['2'])
        self.interaction._out = out_.make_capture()
        self.interaction._in = in_.make_stream()
        self.event.is_done = True
        result = self.interaction.execute(None)
        self.assertEqual(result, 'Come again soon!')

    def test_execute_invalid_choice(self):
        self.interaction.break_out = True
        out_ = fakes.FakeOutput()
        in_ = fakes.FakeInput(['5', '1'])
        self.interaction._out = out_.make_capture()
        self.interaction._in = in_.make_stream()
        self.event.is_done = True
        self.interaction.execute(None)
        self.assertEqual(out_.get_text(),
                         ("\n1. Ask for advice\n"
                          "2. Cancel\n\n"
                          "--------------------------------------------------\n"
                          "Not a valid choice!\n\n"

                          "1. Ask for advice\n"
                          "2. Cancel\n\n"
                          "--------------------------------------------------\n"
                          "Get it while it's hot\n\n"))

    def test_accept(self):
        visitor = fakes.FakeEventVisitor()
        self.interaction.accept(visitor)
        self.assertEqual(visitor.result, self.interaction.id)


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
