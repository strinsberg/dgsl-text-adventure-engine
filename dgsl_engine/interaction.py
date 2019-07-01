from .event_base import Event
from .user_input import Menu


class Interaction(Event):
    def __init__(self, obj_id):
        super(Interaction, self).__init__(obj_id)
        self.options = []

    def execute(self, affected):
        pass

    def add(self, option):
        pass


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
