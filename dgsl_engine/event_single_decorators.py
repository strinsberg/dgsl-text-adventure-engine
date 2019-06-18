from . import event_base


class MessageDecorator(event_base.EventDecorator):
    def __init__(self, event, message):
        super(MessageDecorator, self).__init__(event)
        self.message = message

    def execute(self, affected):
        result = self.event.execute(affected)
        if result != "":
            self.message + '\n' + result
        return self.message