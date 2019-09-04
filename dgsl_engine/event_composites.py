"""Events that are composed of other events."""
from . import event_base
from . import exceptions


class GroupEvent(event_base.Event):
    """An event that holds and executes a group of events all at once.

    Events still execute in the order they are added in.

    Attributes:
        events (Event): The events to execute.
    """

    def __init__(self, obj_id):
        super(GroupEvent, self).__init__(obj_id)
        self.events = []

    def execute(self, affected):
        """Executes all the events it contains and returns the results."""
        results = []

        result = super(GroupEvent, self).execute(affected)
        if result != '':
            results.append(result)

        for event in self.events:
            result = event.execute(affected)
            if result != '':
                results.append(result)

        return "\n".join(results)

    def add(self, event):
        """Add a given event.

        Raises:
            InvalidParameterError: If an event is already in the group.
        """
        for self_event in self.events:
            if event.id == self_event.id:
                raise exceptions.InvalidParameterError(
                    "Already contains event: " + event.id)

        self.events.append(event)

    def accept(self, visitor):
        """Accepts a visitor."""
        visitor.visit_group(self)


class OrderedGroup(GroupEvent):
    """A Group of events that executes events in order one at a time.

    Unlike group only one event is executed at a time.

    Attributes:
        idx (int): The current event to execute.
        last (bool): Weather or not to repeat the final event once all
            events have been executed or to do nothing.
    """

    def __init__(self, obj_id):
        super(OrderedGroup, self).__init__(obj_id)
        self.idx = 0
        self.last = False

    def execute(self, affected):
        """Executes the current event and returns the result."""
        if self.is_done:
            return ''

        res = self.events[self.idx].execute(affected)
        res_super = event_base.Event.execute(self, affected)  # not ok?

        if self.idx < len(self.events) - 1:
            self.idx += 1
        else:
            if self.only_once or self.events[self.idx].is_done:
                self.is_done = True

        if res != '':
            if res_super != '':
                return res_super + '\n' + res
            return res
        return res_super

    def add(self, event):
        """Adds an event to the end of the group.

        Raises:
            InvalidParameterError: If an event is already in the group.
        """
        size = len(self.events)
        if size >= 1:
            self.events[size - 1].only_once = True
        super(OrderedGroup, self).add(event)

    def _check_if_done(self):
        pass


class ConditionalEvent(event_base.Event):
    """Tests a condition and executes a success or failure event.

    Attributes:
        condition (Conditional): The condition to test.
        success (Event): The event to execute if the condition succeeds.
        failure (Event): The event to execute if the condition fails.
        passed (bool): Weather the condition has been satisfied or not.
    """

    def __init__(self, obj_id):
        super(ConditionalEvent, self).__init__(obj_id)
        self.condition = None
        self.success = None
        self.failure = None
        self.passed = False

    def execute(self, affected):
        """Tests the condition and execute the appropriate event."""
        self.passed = False
        succeeded = self.condition.test(affected)

        if succeeded:
            res = self.success.execute(affected)
            self.passed = True
        elif self.failure is not None:
            res = self.failure.execute(affected)
        else:
            res = ''

        res_super = super(ConditionalEvent, self).execute(affected)

        if res != '':
            if res_super != '':
                return res_super + '\n' + res
            return res
        return res_super

    def accept(self, visitor):
        """Accept a visitor."""
        visitor.visit_conditional(self)

    def _check_if_done(self):
        if self.passed and self.only_once:
            self.is_done = True
