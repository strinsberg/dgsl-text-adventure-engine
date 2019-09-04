"""Equipment"""
from .entity_base import Entity


class Equipment(Entity):
    """Equipment that can be worn by Characters.

    Attributes:
        protects (list of str): All the effects the equipment can provide
            protection from.
        slot (str): The slot the equipment goes in. Ie) head, hands, etc.
        must_equip (bool): Wether the equipment must be equipped in order
            to offer protection.
        owner (Character): The character wearing the equipment, or None
            if it is not being worn.
        equipped (bool): Wether or not the equipment is being worn.
    """

    def __init__(self, obj_id):
        super(Equipment, self).__init__(obj_id)
        self.protects = []
        self.slot = "empty"
        self.must_equip = True
        self.owner = None
        self.equipped = False

    def accept(self, visitor):
        """Accepts a visitor"""
        visitor.visit_equipment(self)

    def __repr__(self):
        return "<Equipment: '{}', Name: '{}'>".format(
            self.spec.id, self.spec.name)
