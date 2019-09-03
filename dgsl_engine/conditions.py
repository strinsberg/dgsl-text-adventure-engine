"""Conditions to test the player or other entities with."""
from . import collectors


class Question:  # pylint: disable=too-few-public-methods
    """Question"""

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self._in = input

    def test(self, entity):  # pylint: disable=unused-argument
        """

        Args:
          entity:

        Returns:

        """
        print(self.question)
        ans = self._in("Answer: ")
        print()
        if ans.strip().lower() == self.answer.lower():
            return True
        return False


class HasItem:  # pylint: disable=too-few-public-methods
    """Has Item"""

    def __init__(self, item_id, other_json=None, world=None):
        self.item_id = item_id
        self.other = None
        if other_json is not None and world is not None:
            collector = collectors.EntityIdCollector(other_json['id'], world)
            self.other = collector.collect()

    def test(self, container):
        """

        Args:
          container:

        Returns:

        """
        if self.other is None:
            item = container.get(self.item_id)
        else:
            item = self.other.get(self.item_id)

        if item is not None:
            return True
        return False


class Protected:  # pylint: disable=too-few-public-methods
    """Protected"""

    def __init__(self, effects):
        self.effects = effects

    def test(self, character):
        """

        Args:
          character:

        Returns:

        """
        not_equipped = _get_valid_carried(character)
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


def _get_valid_carried(character):
    """

    Args:
    character:

    Returns:

    """
    collector = collectors.EntityTypeCollector(['equipment'], character)
    equipment = collector.collect()
    results = []
    for equip in equipment:
        if not equip.must_equip and not equip.equipped:
            results.append(equip)
    return results


class IsActive:  # pylint: disable=too-few-public-methods
    """empty"""

    def __init__(self, entity):
        self.entity = entity

    def test(self, _=None):
        """empty"""
        return self.entity.states.active
