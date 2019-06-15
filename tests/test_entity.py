import unittest
import dgsl_engine.entity as entity

ID = "1234"


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.entity = entity.Entity(ID)

    def test_init(self):
        self.assertEqual(self.entity.spec.id, ID)
        self.assertEqual(self.entity.spec.name, "Null")
        self.assertEqual(self.entity.states.active, True)
        self.assertFalse(self.entity.events.events)

    def test_describe(self):
        description = "A nice entity"
        self.entity.spec.description = description
        self.assertEqual(self.entity.describe(), description)


if __name__ == '__main__':
    unittest.main()