from . import event_base
from . import exceptions


class GroupEvent(event_base.Event):
    def __init__(self, obj_id):
        super(GroupEvent, self).__init__(obj_id)
        self.events = []

    def execute(self, affected):
        results = []

        for event in self.events:
            r = event.execute()
            if r != '':
                results.append(r)

        r = super(GroupEvent).execute(affected)
        if r != '':
            results.append(r)

        return "\n".join(results)

    def add(self, event):
        if event not in self.events:
            self.events.append(event)
        else:
            raise exceptions.InvalidParameterError(
                "Already contains event: " + event.id)
