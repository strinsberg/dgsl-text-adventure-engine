class Parser:
    def parse(self, user_input):
        words = user_input.strip().split()
        return {'verb': words[0], 'subject': " ".join(words[1:])}


class Collector:
    pass


class Menu:
    pass
