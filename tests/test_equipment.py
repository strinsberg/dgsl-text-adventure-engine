import unittest
import unittest.mock as mock
import dgsl_engine.equipment as equipment

# Constants ############################################################

ID = "03ru02r0"
SLOT = 'head'
PROTECTS = ['cold', 'wind']
MUST = 0


# Tests ################################################################

class TestEquipment(unittest.TestCase):
    def setUp(self):
        self.equipment = equipment.Equipment(ID)
        self.equipment.slot = SLOT
        self.equipment.protects = PROTECTS
        self.equipment.must_equip = MUST

    def test_init(self):
        self.assertEqual(self.equipment.slot, SLOT)
        self.assertEqual(self.equipment.protects, PROTECTS)
        self.assertEqual(self.equipment.must_equip, MUST)

    def test_accept(self):
        visitor = mock.MagicMock()
        self.equipment.accept(visitor)
        visitor.visit_equipment.assert_called_with(self.equipment)

    def test_repr(self):
        rep = "<Equipment: '{}', Name: '{}'>".format(
            self.equipment.spec.id, self.equipment.spec.name)
        self.assertEqual(repr(self.equipment), rep)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
