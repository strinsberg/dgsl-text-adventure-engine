"""Conditions to test the player or other entities with."""
from . import collectors


class Question:  # pylint: disable=too-few-public-methods
    """A Condition that asks a question and succeeds only if the playr
    gives the right answer.

    Attributes:
        question (str): The question to ask.
        answer (str): The correct answer to the question.
    """

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self._in = input

    def test(self, _=None):
        """Asks the question and evaluates the given answer.

        Args:
          _: Placeholder to maintain Condition.test interface which
            requires an entity.

        Returns:
            bool: True if the player gives the correct answer, otherwise
                False.
        """
        print(self.question)
        ans = self._in("Answer: ")
        print()
        if ans.strip().lower() == self.answer.lower():
            return True
        return False


class HasItem:  # pylint: disable=too-few-public-methods
    """A Condition that checks a container to see if it contains a
    specific item.

    Can do this for the entity passed to test or for an entity set up
    during world creation. This allows seeing if the player has an
    item or if items have been taken from, or added to, other containers
    during the course of the game.

    Attributes:
        item_id (str): The item of the id to check for.
        other (Container): A container to check for the item. If this is
            None then the container(usually the player) passed to test
            will be checked.
        other_json (dict): The json object for the other from the .world
            file used in world creation.
        world (World): A world object. Needs to already have all entities
            constructed (though not necessarily fully assembled).
    """

    def __init__(self, item_id, other_json=None, world=None):
        self.item_id = item_id
        self.other = None
        if other_json is not None and world is not None:
            collector = collectors.EntityIdCollector(other_json['id'], world)
            self.other = collector.collect()

    def test(self, container):
        """Test the given container or self.other for the desired item.

        Args:
          container (Container): The container to check if other is None.
            This is generally the player.

        Returns:
            bool: True if the object is found, otherwise false.
        """
        if self.other is None:
            item = container.get(self.item_id)
        else:
            item = self.other.get(self.item_id)

        if item is not None:
            return True
        return False


class Protected:  # pylint: disable=too-few-public-methods
    """Checks a character to see if they are protected from a set of
    effects.

    Attributes:
        effects (list of str): A list of the effects to test for protection.
    """

    def __init__(self, effects):
        self.effects = effects

    def test(self, character):
        """Tests the character to make sure they are protected from all
        the effects.

        Args:
          character (Character): The character to check is protected.

        Returns:
            bool: True if the character is protected from ALL the effects,
                otherwise False.
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
    """Get all equipment that may offer protection from a player's
    inventory or that they have equipped.

    This is necessary because some equipment must be equipped in order
    to offer protection and some equipment can offer protection as long
    as it is being carried by the player.

    Args:
        character (Character): The character to get equipment from.

    Returns:
        A list of Equipment that may offer protection.
    """
    collector = collectors.EntityTypeCollector(['equipment'], character)
    equipment = collector.collect()
    results = []
    for equip in equipment:
        if not equip.must_equip and not equip.equipped:
            results.append(equip)
    return results


class IsActive:  # pylint: disable=too-few-public-methods
    """Checks to see if an entity is active.

    Though it is almost trivial, using an object for this allows it to
    be attached to Events and Interaction Options easily.

    Attributes:
        entity (Entity): The entity to check is active."""

    def __init__(self, entity):
        self.entity = entity

    def test(self, _=None):
        """Returns the Truth value of the entity's active state.

        Args:
            _: Placeholder to maintain Condition interface.

        Returns:
            bool: True if the entity is active, otherwise False."""
        return self.entity.states.active
