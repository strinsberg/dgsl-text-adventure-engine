from . import event_base
from . import exceptions


class GroupEvent(event_base.Event):
    def __init__(self, obj_id):
        super(GroupEvent, self).__init__(obj_id)
        self.events = []

    def execute(self, affected):
        results = []

        for event in self.events:
            r = event.execute(affected)
            if r != '':
                results.append(r)

        r = super(GroupEvent, self).execute(affected)
        if r != '':
            results.append(r)

        return "\n".join(results)

    def add(self, event):
        for e in self.events:
            if event.id == e.id:
                raise exceptions.InvalidParameterError(
                    "Already contains event: " + event.id)

        self.events.append(event)


class OrderedGroup(GroupEvent):
    def __init__(self, obj_id):
        super(OrderedGroup, self).__init__(obj_id)
        self.idx = 0

    def execute(self, affected):
        if self.events[self.idx].is_done:
            if self.idx < len(self.events) - 1:
                self.idx += 1
            else:
                return 'Nothing happens'

        res = self.events[self.idx].execute(affected)
        res_super = event_base.Event.execute(self, affected)  # not ok?

        if res != '':
            if res_super != '':
                return res + '\n' + res_super
            return res
        return res_super

    def add(self, event):
        size = len(self.events)
        if size >= 1:
            self.events[size - 1].only_once = True
        super(OrderedGroup, self).add(event)


class ConditionalEvent(event_base.Event):
    def __init__(self, obj_id):
        super(ConditionalEvent, self).__init__(obj_id)
        self.condition = None
        self.success = None
        self.failure = None

    def execute(self, affected):
        succeeded = self.condition.test(affected)
        res_super = super(ConditionalEvent, self).execute(affected)

        if succeeded:
            res = self.success.execute(affected)
            if self.only_once:
                self.is_done = True
        elif self.failure is not None:
            res = self.failure.execute(affected)
        else:
            res = ''

        if res != '':
            if res_super != '':
                return res + '\n' + res_super
            return res
        return res_super
