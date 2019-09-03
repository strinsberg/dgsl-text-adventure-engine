import unittest
from unittest import mock
from contextlib import redirect_stdout
from io import StringIO
import dgsl_engine.interaction as interaction


class TestInteraction(unittest.TestCase):
    def setUp(self):
        self.event = mock.MagicMock(is_done=False)
        self.event.execute.return_value = 'Have some free advice'
        self.other_event = mock.MagicMock(is_done=False)
        self.other_event.execute.return_value = 'Thank you for the help'
        self.condition = mock.MagicMock()

        self.interaction = interaction.Interaction('2342308')
        self.option = interaction.Option(
            'Ask for advice', self.event, breakout=True)
        self.cond_option = interaction.ConditionalOption(
            'Fix the reactor', self.other_event, self.condition, breakout=True)
        self.interaction.add(self.option)
        self.interaction.add(self.cond_option)

        self.str_out = StringIO()

    def tearDown(self):
        self.str_out.close()

    @mock.patch('dgsl_engine.user_input.Menu')
    def test_execute_option_1(self, mock_menu):
        mock_menu.return_value.ask.return_value = 0

        with redirect_stdout(self.str_out):
            self.interaction.execute(None)

        self.assertEqual(
            self.str_out.getvalue(),
            ("\n\n--------------------------------------------------\n"
             "Have some free advice\n"))

    @mock.patch('dgsl_engine.user_input.Menu')
    def test_execute_option_2(self, mock_menu):
        mock_menu.return_value.ask.return_value = 1

        with redirect_stdout(self.str_out):
            self.interaction.execute(None)

        self.assertEqual(
            self.str_out.getvalue(),
            ("\n\n--------------------------------------------------\n"
             "Thank you for the help\n"))

    @mock.patch('dgsl_engine.user_input.Menu')
    def test_execute_cancelled(self, mock_menu):
        mock_menu.return_value.ask.return_value = 2

        with redirect_stdout(self.str_out):
            self.interaction.execute(None)

        self.assertEqual(
            self.str_out.getvalue(),
            ("\n\n--------------------------------------------------\n"
             "Cancelled\n"))

    @mock.patch('dgsl_engine.user_input.Menu')
    def test_execute_not_a_choice(self, mock_menu):
        mock_menu.return_value.ask.side_effect = [-1, 2]

        with redirect_stdout(self.str_out):
            self.interaction.execute(None)

        self.assertEqual(
            self.str_out.getvalue(),
            ("\n\n--------------------------------------------------\n"
             "Not a valid choice!\n\n"
             "\n--------------------------------------------------\n"
             "Cancelled\n"))

    @mock.patch('dgsl_engine.user_input.Menu')
    def test_execute_messages(self, mock_menu):
        self.interaction.message = "Something before the menu"
        self.interaction.end_message = "Something before you go"
        mock_menu.return_value.ask.return_value = 1

        with redirect_stdout(self.str_out):
            self.interaction.execute(None)

        self.assertEqual(
            self.str_out.getvalue(),
            ("Something before the menu\n\n"
             "\n--------------------------------------------------\n"
             "Thank you for the help\n\n"
             "Something before you go\n"))

    def test_accept(self):
        visitor = mock.MagicMock()
        self.interaction.accept(visitor)
        visitor.visit_interaction.assert_called_with(self.interaction)


class TestOption(unittest.TestCase):
    def setUp(self):
        self.event = mock.MagicMock()
        self.option = interaction.Option('Ask for advice', self.event)

    def test_is_visible(self):
        self.event.is_done = False
        vis = self.option.is_visible(None)
        self.assertTrue(vis)

    def test_is_visible_false(self):
        self.event.is_done = True
        vis = self.option.is_visible(None)
        self.assertFalse(vis)

    def test_choose(self):
        self.event.execute.side_effect = ["Executed event", False]
        result, breakout = self.option.choose(None)
        self.assertEqual(result, "Executed event")
        self.assertFalse(breakout)

    def test_repr(self):
        rep = "<Option - Text: '{}'>".format(self.option.text)
        self.assertEqual(repr(self.option), rep)


class TestConditionalOption(unittest.TestCase):
    def setUp(self):
        self.event = mock.MagicMock()
        self.condition = mock.MagicMock()
        self.option = interaction.ConditionalOption(
            'Ask for advice', self.event, self.condition)

    @mock.patch('dgsl_engine.interaction.Option.is_visible')
    def test_is_visible(self, mock_is_visible):
        mock_is_visible.return_value = True
        self.condition.test.return_value = True

        vis = self.option.is_visible(None)
        self.assertTrue(vis)

    @mock.patch('dgsl_engine.interaction.Option.is_visible')
    def test_is_visible_false(self, mock_is_visible):
        mock_is_visible.return_value = False

        vis = self.option.is_visible(None)
        self.assertFalse(vis)

    @mock.patch('dgsl_engine.interaction.Option.is_visible')
    def test_is_visible_is_done(self, mock_is_visible):
        mock_is_visible.return_value = True
        self.condition.test.return_value = False

        vis = self.option.is_visible(None)
        self.assertFalse(vis)

    def test_repr(self):
        rep = ("<Conditional Option - Text: '{}', "
               "Condition: '{}'>").format(
            self.option.text, self.condition)
        self.assertEqual(repr(self.option), rep)
