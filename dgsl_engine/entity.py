import event


class Entity:
    def __init__(self, obj_id: str):
        self.spec = Spec(obj_id)
        self.states = States()
        self.events = Events()

    def describe(self) -> str:
        return self.spec.description

    def accept(self, visitor) -> None:
        pass


class Spec:
    def __init__(self, obj_id):
        self.id = obj_id
        self.name = ""
        self.description = ""

    def matches(self, spec: Spec) -> bool:
        return spec.id == self.id


class States:
    def __init__(self):
        self.active = True
        self.obtainable = True
        self.hidden = False


class Events:
    def __init__(self):
        self.events = {}

    def add(self, event: event.Event) -> None:
        self.events[event.verb] = event

    def execute(self, verb: str, entity: Entity) -> str:
        return self.events[verb].execute(entity)

    def has_event(self, verb: str) -> bool:
        return verb in self.events
