import unittest
import dgsl_engine.event_base as event_base
import dgsl_engine.entity_base as entity_base
import dgsl_engine.entity_containers as containers
from . import fakes

ID = '1234'
ID2 = "5678"
ID3 = "9876"
ID4 = "5432"
ID5 = "entity"
RESULT = ''

# Tests ################################################################


class TestEventBase(unittest.TestCase):
    def setUp(self):
        self.event = event_base.Event(ID)
        self.other_event = event_base.Event(ID)
        self.entity = entity_base.Entity(ID)

    def test_init(self):
        self.assertFalse(self.event.is_done)
        self.assertFalse(self.event.only_once)

    def test_execute(self):
        # Will need to change when event gets subjects
        self.assertEqual(self.event.execute(self.entity), RESULT)

    def test_visit(self):
        visitor = fakes.FakeVisitor()
        self.event.accept(visitor)
        self.assertEqual(visitor.result, ID)

    def test_register(self):
        self.event.register(self.other_event)
        self.assertIn(self.other_event, self.event.subjects)


# Tests ################################################################


class TestMoveEntity(unittest.TestCase):
    def setUp(self):
        self.entity = entity_base.Entity(ID5)
        self.container = containers.Container(ID)
        self.room = containers.Room(ID2)
        self.player = containers.Player(ID3)
        self.move = event_base.MoveEntity(ID4)

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
        with self.assertRaises(containers.ContainerError):
            self.move.execute(self.player)
        self.assertTrue(self.room.inventory.has_item(ID3))
        self.assertFalse(self.container.inventory.has_item(ID3))

    def test_visit(self):
        visitor = fakes.FakeVisitor()
        self.move.accept(visitor)
        self.assertEqual(visitor.result, ID4)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()