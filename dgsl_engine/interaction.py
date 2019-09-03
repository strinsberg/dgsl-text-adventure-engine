"""Interaction event"""
from . import event_base
from . import user_input


class Interaction(event_base.Event):
    """An to facilitate an interaction between the player and an entity.

    Events are added in options with text. The text is displayed in a
    menu and the Player can choose which option they want. Some options
    can be conditional so they will only show if certain conditions
    are met. Events that are marked as done will also not be present in
    the menu.

    Attributes:
        options: A list of options.
        break_out (bool): True if after a choice the menu does not
            appear again, otherwise the menu will be displayed again
            after every choice until cancelled.
        end_message (str): A message to display when the interaction is
            finished.
    """

    def __init__(self, obj_id):
        super(Interaction, self).__init__(obj_id)
        self.options = []
        self.break_out = False
        self.end_message = None

    def execute(self, affected):
        """Run the interaction displaying the menu and results of the
        chosen events.
        """
        # This may not be ideal
        if self.message is not None and self.message != '':
            print(self.message)

        while True:
            options, choices = self._make_choices(affected)
            menu = user_input.Menu(choices)

            print()
            idx = menu.ask()
            print(
                '\n--------------------------------------------------')

            if idx >= len(choices):
                if self.end_message is None:
                    print('Cancelled')
                break
            elif idx < 0:
                print('Not a valid choice!')
                continue
            else:
                result, end = options[idx].choose(affected)
                print(result)

            if self.break_out or end:
                break

        if self.end_message is not None and self.end_message.strip() != '':
            print()
            print(self.end_message)
        return ''

    def add(self, option):
        """Add an option to the interaction."""
        self.options.append(option)

    def _make_choices(self, affected):
        """Create the list of choices for the menu filtering out those
        options that should not be visible.
        """
        options = []
        choices = []
        for opt in self.options:
            if opt.is_visible(affected):
                options.append(opt)
                choices.append(opt.text)
        return options, choices

    def accept(self, visitor):
        """Accept a visitor."""
        visitor.visit_interaction(self)


class Option:
    """An option containing menu text and an event.

    Attributes:
        text (str): The text to display in a menu.
        event (Event): The event to execute if the option is chosen.
        breakout (bool): Weather the option should force the
            interaction to breakout."""

    def __init__(self, text, event, breakout=False):
        self.text = text
        self.event = event
        self.breakout = breakout

    def is_visible(self, affected):  # pylint: disable=unused-argument
        """Check an option to see if it should be shown."""
        if self.event.is_done:
            return False
        return True

    def choose(self, affected):
        """Execute the options event."""
        return self.event.execute(affected), self.breakout

    def __repr__(self):
        return "<Option - Text: '{}'>".format(self.text)


class ConditionalOption(Option):
    """An option that also has a condition to determine its visibility.

    Attributes:
        condition (Condition): The condition to check.
    """

    def __init__(self, text, event, condition, breakout=False):
        super(ConditionalOption, self).__init__(text, event, breakout)
        self.condition = condition

    def is_visible(self, affected):
        """Check to see if the option should be shown."""
        super_success = super(ConditionalOption, self).is_visible(affected)
        if super_success:
            return self.condition.test(affected)
        return False

    def __repr__(self):
        return "<Conditional Option - Text: '{}', Condition: '{}'>".format(
            self.text, self.condition)
