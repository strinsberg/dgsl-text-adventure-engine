import unittest
import dgsl_engine.entity_containers as container
import dgsl_engine.event_single as single
import dgsl_engine.entity_base as entity

ID = "1234"
ID2 = "5678"
ID3 = "9876"
ID4 = "5432"
ID5 = "entity"


class TestMoveEntity(unittest.TestCase):
    def setUp(self):
        self.entity = entity.Entity(ID5)
        self.container = container.Container(ID)
        self.room = container.Room(ID2)
        self.player = container.Player(ID3)
        self.move = single.MoveEntity(ID4)

    def test_init(self):
        self.move.id = ID4

    def test_execute(self):
        self.container.add(self.entity)
        self.move.destination = self.room
        self.move.execute(self.entity)
        self.assertTrue(self.room.inventory.has_item(ID5))
        self.assertFalse(self.container.inventory.has_item(ID5))

    def test_execute_raises(self):
        self.room.add(self.player)
        self.move.destination = self.container
        with self.assertRaises(container.ContainerError):
            self.move.execute(self.player)
        self.assertTrue(self.room.inventory.has_item(ID3))
        self.assertFalse(self.container.inventory.has_item(ID3))


# Main #################################################################

if __name__ == '__main__':
    unittest.main()