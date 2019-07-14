import unittest
import dgsl_engine.equipment as equipment
import dgsl_engine.entity_factory as ent_fact
from . import json_objects


class TestEquipment(unittest.TestCase):
    def setUp(self):
        self.equipment = ent_fact.EntityFactory().new(json_objects.EQUIPMENT)

    def test_init(self):
        pass

    def test_accept(self):
        pass

    def test_repr(self):
        rep = "<Equipment: '{}', Name: '{}'>".format(
            self.equipment.spec.id, self.equipment.spec.name)
        self.assertEqual(repr(self.equipment), rep)
