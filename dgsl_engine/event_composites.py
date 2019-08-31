"""Events that are composed of other events."""
from . import event_base
from . import exceptions


class GroupEvent(event_base.Event):
    """Group"""

    def __init__(self, obj_id):
        super(GroupEvent, self).__init__(obj_id)
        self.events = []

    def execute(self, affected):
        """

        Args:
          affected:

        Returns:

        """
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
        """

        Args:
          event:

        Returns:

        """
        for self_event in self.events:
            if event.id == self_event.id:
                raise exceptions.InvalidParameterError(
                    "Already contains event: " + event.id)

        self.events.append(event)

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_group(self)


class OrderedGroup(GroupEvent):
    """Ordered"""

    def __init__(self, obj_id):
        super(OrderedGroup, self).__init__(obj_id)
        self.idx = 0
        self.last = False

    def execute(self, affected):
        """

        Args:
          affected:

        Returns:

        """
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
        """

        Args:
          event:

        Returns:

        """
        size = len(self.events)
        if size >= 1:
            self.events[size - 1].only_once = True
        super(OrderedGroup, self).add(event)

    def _check_if_done(self):
        pass


class ConditionalEvent(event_base.Event):
    """Conditional"""

    def __init__(self, obj_id):
        super(ConditionalEvent, self).__init__(obj_id)
        self.condition = None
        self.success = None
        self.failure = None
        self.passed = False

    def execute(self, affected):
        """

        Args:
          affected:

        Returns:

        """
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
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_conditional(self)

    def _check_if_done(self):
        if self.passed and self.only_once:
            self.is_done = True
