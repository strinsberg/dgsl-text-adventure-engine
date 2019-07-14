"""Conditions to test the player or other entities with."""
from . import visitors


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


class Protected:
    def __init__(self, effects):
        self.effects = effects

    def test(self, character):
        not_equipped = self._get_valid_carried(character)
        protected = set()
        for effect in self.effects:
            protected = False

            for equipment in character.equipped:
                if effect in equipment.protects:
                    protected = True
                    break

            if not protected:
                for equipment in not_equipped:
                    if effect in equipment.protects:
                        protected = True
                        break

            if not protected:
                return False
        return True

    def _get_valid_carried(self, character):
        collector = visitors.EntityTypeCollector(['equipment'], character)
        equipment = collector.collect()
        results = []
        for equip in equipment:
            if not equip.must_equip and not equip.equipped:
                print(equip)
                results.append(equip)
        return results
