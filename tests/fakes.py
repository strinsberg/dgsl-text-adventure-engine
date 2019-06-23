class FakeCollector:
    """Fake collector and factory.
    
    Factory returns itself. Collect returns a list of integers."""

    def __init__(self, n):
        self.n = n

    def make(self, *args):
        return self

    def collect(self):
        return [x for x in range(self.n)]


class FakeMenu:
    """Fake menu and factory.
    
    Factory returns itself. Menu returns the constructor value."""

    def __init__(self, n):
        self.n = n

    def make(self, *args):
        return self

    def ask(self, *args):
        return self.n


class FakeAction:
    """Fake action and factory.
    
    Factory returns itself. action returns strings based on params to new."""

    def new(self, verb, player, entity, other):
        self.entity = entity
        return self

    def take_action(self):
        if self.entity is None:
            return "Verb with no object"
        return "Result found"