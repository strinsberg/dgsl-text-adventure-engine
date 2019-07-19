"""Interaction event"""
from .event_base import Event
from .user_input import Menu


class Interaction(Event):
    """ Interaction"""

    def __init__(self, obj_id):
        super(Interaction, self).__init__(obj_id)
        self.options = []
        self.break_out = False
        self.end_message = None
        self._in = input
        self._out = print

    def execute(self, affected):
        """

        Args:
          affected:

        Returns:

        """
        # This may not be ideal
        if self.message is not None and self.message != '':
            self._out(self.message + '\n')

        while True:
            options, choices = self._make_choices(affected)
            menu = Menu(choices, self._out, self._in)

            # self._out()
            idx = menu.ask()

            self._out(
                '\n--------------------------------------------------')

            if idx >= len(choices):
                if self.end_message is None:
                    self._out('Cancelled')
                else:
                    self._out(self.end_message)
                break
            elif idx < 0:
                self._out('Not a valid choice!\n')
                continue
            else:
                result, end = options[idx].choose(affected)
                self._out(result)

            self._out()
            if self.break_out or end:
                break

        return ''

    def add(self, option):
        """

        Args:
          option:

        Returns:

        """
        self.options.append(option)

    def _make_choices(self, affected):
        """

        Args:
          affected:

        Returns:

        """
        options = []
        choices = []
        for opt in self.options:
            if opt.is_visible(affected):
                options.append(opt)
                choices.append(opt.text)
        return options, choices

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_interaction(self)


class Option:
    """ option"""

    def __init__(self, text, event, breakout=False):
        self.text = text
        self.event = event
        self.breakout = breakout

    def is_visible(self, affected):  # pylint: disable=unused-argument
        """

        Args:
          affected:

        Returns:

        """
        if self.event.is_done:
            return False
        return True

    def choose(self, affected):
        """

        Args:
          affected:

        Returns:

        """
        return self.event.execute(affected), self.breakout

    def __repr__(self):
        return "<Option - Text: '{}'>".format(self.text)


class ConditionalOption(Option):
    """conditional """

    def __init__(self, text, event, condition, breakout=False):
        super(ConditionalOption, self).__init__(text, event, breakout)
        self.condition = condition

    def is_visible(self, affected):
        """

        Args:
          affected:

        Returns:

        """
        super_success = super(ConditionalOption, self).is_visible(affected)
        if super_success:
            return self.condition.test(affected)
        return False

    def __repr__(self):
        return "<Conditional Option - Text: '{}', Condition: '{}'>".format(
            self.text, self.condition)
