import unittest
import dgsl_engine.entity_containers as container
import dgsl_engine.entity_base as entity

ID = "1234"


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = container.Container(ID)
        self.entity = entity.Entity(ID)
        self.room = container.Room(ID)
        self.player = container.Player(ID)

    def test_add_entity(self):
        self.assertTrue(self.container.add(self.entity))
        self.assertEqual(self.entity.owner, self.container)

    def test_iter(self):
        self.container.add(self.entity)
        result = ""
        for item in self.container:
            result += item.spec.id
        self.assertEqual(result, ID)

    def test_add_throws(self):
        with self.assertRaises(container.ContainerError):
            self.container.add(self.player)
        with self.assertRaises(container.ContainerError):
            self.container.add(self.room)


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.container = container.Room(ID)
        self.room = container.Room(ID)

    def test_add_entity(self):
        ent = entity.Entity(ID)
        self.assertTrue(self.container.add(ent))
        self.assertEqual(ent.owner, self.container)

    def test_add_throws(self):
        with self.assertRaises(container.ContainerError):
            self.container.add(self.room)


class TestPlayer(unittest.TestCase):
    pass
    # Will add tests when more functionality is added to the player


if __name__ == '__main__':
    unittest.main()