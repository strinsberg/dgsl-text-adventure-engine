class Event:
    def __init__(self, obj_id):
        self.id = obj_id
        self.verb = None

    def execute(self, entity):
        raise NotImplementedError
