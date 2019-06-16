import unittest
import dgsl_engine.entity_containers as container
import dgsl_engine.entity_base as entity

ID = "1234"


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = container.Container(ID)
        self.entity = entity.Entity(ID)
        self.container.inventory.add(self.entity)

    def test_init(self):
        self.assertTrue(self.container.inventory.has_item(ID))


class TestRoom(unittest.TestCase):
    pass
    # Not really anythong to test yet


class TestPlayer(unittest.TestCase):
    pass
    # Not really anything to test yet


if __name__ == '__main__':
    unittest.main()