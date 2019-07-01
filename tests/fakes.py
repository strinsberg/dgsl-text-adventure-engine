class FakeVisitor:
    def visit_event(self, event):
        self.result = event.id

    def visit_move(self, event):
        self.visit_event(event)


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


class FakeOutput:
    def __init__(self):
        self.text = []

    def make_capture(self):
        return self.capture

    def get_text(self):
        return "".join(self.text)

    def capture(self, text=None):
        out = text + '\n' if text is not None else '\n'
        self.text.append(out)


class FakeInput:
    def __init__(self, text_list):
        self.text_list = text_list
        self.prompts = []
        self.idx = -1

    def make_stream(self):
        return self.next

    def next(self, prompt):
        self.prompts.append(prompt)
        self.idx += 1
        return self.text_list[self.idx]


class FakeResolver:
    def __init__(self, results):
        self.results = results
        self.idx = -1

    def resolve_input(self, input, player):
        self.idx += 1
        return self.results[self.idx]


class FakeCondition:
    def __init__(self, result):
        self.result = result

    def test(self, affected):
        return self.result
