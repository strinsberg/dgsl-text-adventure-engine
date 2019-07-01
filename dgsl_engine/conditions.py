"""Conditions to test the player or other entities with."""


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self._in = input
        self._out = print

    def test(self, entity):
        self._out(self.question)
        ans = self._in("Answer: ")
        if ans.strip() == self.answer:
            return True
        return False


class HasItem:
    def __init__(self, item_id):
        self.item_id = item_id

    def test(self, container):
        item = container.get(self.item_id)
        if item is not None:
            return True
        return False
