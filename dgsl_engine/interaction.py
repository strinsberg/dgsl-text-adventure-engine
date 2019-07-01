from .event_base import Event
from .user_input import Menu


class Interaction(Event):
    def __init__(self, obj_id):
        super(Interaction, self).__init__(obj_id)
        self.options = []
        self.break_out = False
        self._in = input
        self._out = print

    def execute(self, affected):
        choices = self._make_choices(affected)
        menu = Menu(choices, self._out, self._in)

        while True:
            self._out('\n')
            idx = menu.ask() - 1

            if idx >= len(choices):
                self._out('\n')
                break

            self._out(
                '\n--------------------------------------------------\n')

            if idx < 0:
                self._out('Not a valid choice!\n')
                continue
            else:
                self._out(self.options[idx].choose(affected) + '\n')

            if self.break_out:
                self._out('\n')
                break

        return super(Interaction, self).execute(affected)

    def add(self, option):
        self.options.append(option)

    def _make_choices(self, affected):
        choices = []
        for opt in self.options:
            if opt.is_visible(affected):
                choices.append(opt.text)
        return choices


class Option:
    def __init__(self, text, event):
        self.text = text
        self.event = event

    def is_visible(self, affected):
        if self.event.is_done:
            return False
        return True

    def choose(self, affected):
        return self.event.execute(affected)


class ConditionalOption(Option):
    def __init__(self, text, event, condition):
        super(ConditionalOption, self).__init__(text, event)
        self.condition = condition

    def is_visible(self, affected):
        super_success = super(ConditionalOption, self).is_visible(affected)

        if super_success:
            return self.condition.test(affected)
        return False
