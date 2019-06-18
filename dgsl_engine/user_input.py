class Parser:
    def parse(self, user_input):
        words = user_input.strip().split()
        return {'verb': words[0], 'subject': " ".join(words[1:])}


class Collector:
    """Visitor that collects all items that match with player input."""

    def __init__(self, parsed_command):
        self.parsed = parsed_command
        self.entities = []

    def visit_entity(self, entity):
        if entity.spec.name.find(self.parsed['subject']) > -1:
            self.entities.append(entity)

    def visit_container(self, container):
        self.visit_entity(container)
        for item in container:
            item.accept(self)


class Menu:
    pass
