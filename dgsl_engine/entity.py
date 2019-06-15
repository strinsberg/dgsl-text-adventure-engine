class Entity:
    def __init__(self, obj_id):
        self.spec = Spec(obj_id)
        self.states = States()
        self.events = Events()

    def describe(self):
        return self.spec.description


class Spec:
    def __init__(self, obj_id):
        self.id = obj_id
        self.name = "Null"
        self.description = "Null"

    def matches(self, spec):
        return spec.id == self.id


class States:
    def __init__(self):
        self.active = True
        self.obtainable = True
        self.hidden = False


class Events:
    def __init__(self):
        self.events = {}

    def add(self, event):
        self.events[event.verb] = event

    def execute(self, verb, entity):
        return self.events[verb].execute(entity)

    def has_event(self, verb):
        return verb in self.events
