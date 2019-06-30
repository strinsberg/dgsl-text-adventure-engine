import unittest
import dgsl_engine.entity_containers as container
import dgsl_engine.entity_base as entity

ID = "1234"

# Mocks ################################################################


class MockVisitor:
    def visit_container(self, container):
        self.result = container.spec.id


# Tests ################################################################


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = container.Container(ID)
        self.entity = entity.Entity(ID)
        self.room = container.Room(ID)
        self.player = container.Player(ID)

    def test_add_entity(self):
        self.assertTrue(self.container.add(self.entity))
        self.assertEqual(self.entity.owner, self.container)

    def test_get_item_there(self):
        self.container.add(self.entity)
        self.assertIs(self.container.get(self.entity.spec.id), self.entity)

    def test_get_item_not_there(self):
        self.assertIs(self.container.get(self.entity.spec.id), None)

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

    def test_add_already_there(self):
        self.container.add(self.entity)
        self.assertFalse(self.container.add(self.entity))

    def test_visit(self):
        visitor = MockVisitor()
        self.container.accept(visitor)
        self.assertEqual(visitor.result, ID)


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = container.Room(ID)
        self.other_room = container.Room(ID)

    def test_init(self):
        self.assertTrue(self.room.states.active)
        self.assertFalse(self.room.states.obtainable)
        self.assertFalse(self.room.states.hidden)

    def test_add_entity(self):
        ent = entity.Entity(ID)
        self.assertTrue(self.room.add(ent))
        self.assertEqual(ent.owner, self.room)

    def test_add_throws(self):
        with self.assertRaises(container.ContainerError):
            self.room.add(self.other_room)

    def test_add_already_there(self):
        ent = entity.Entity(ID)
        self.room.add(ent)
        self.assertFalse(self.room.add(ent))


class TestPlayer(unittest.TestCase):
    pass
    # Will add tests when more functionality is added to the player


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
