"""Equipment"""
from .entity_base import Entity


class Equipment(Entity):
    """Equipment"""

    def __init__(self, obj_id):
        super(Equipment, self).__init__(obj_id)
        self.protects = []
        self.slot = "empty"
        self.must_equip = True
        self.owner = None
        self.equipped = False

    def accept(self, visitor):
        """

        Args:
          visitor:

        Returns:

        """
        visitor.visit_equipment(self)

    def __repr__(self):
        return "<Equipment: '{}', Name: '{}'>".format(
            self.spec.id, self.spec.name)
