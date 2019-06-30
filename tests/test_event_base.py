import unittest
import dgsl_engine.event_base as event_base
import dgsl_engine.entity_base as entity_base
import dgsl_engine.entity_containers as containers
import dgsl_engine.event_factory as event_factory
import dgsl_engine.entity_factory as entity_factory
from . import fakes
from . import json_objects as objects

ID = '1234'
ID2 = "5678"
ID3 = "9876"
ID4 = "5432"
ID5 = "entity"
RESULT = ''

# Tests ################################################################


class TestEvent(unittest.TestCase):
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

    def test_repr(self):
        rep = "<Event '{}'>".format(self.event.id)
        self.assertEqual(self.event.__repr__(), rep)


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

    def test_repr(self):
        rep = "<Move '{}'>".format(self.move.id)
        self.assertEqual(self.move.__repr__(), rep)


class TestGive(unittest.TestCase):
    def setUp(self):
        self.ent_fact = entity_factory.EntityFactory()
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.container.add(self.entity)
        self.player = self.ent_fact.new(objects.PLAYER)

        self.evt_fact = event_factory.EventFactory()
        self.give = self.evt_fact.new(objects.GIVE)
        self.give.item_id = self.entity.spec.id
        self.give.owner = self.container

    def test_execute(self):
        self.assertIs(self.container.get(self.entity.spec.id), self.entity)
        self.give.execute(self.player)
        self.assertIs(self.container.get(self.entity.spec.id), None)
        self.assertIs(self.player.get(self.entity.spec.id), self.entity)

    def test_repr(self):
        rep = "<Give '{}'>".format(self.give.id)
        self.assertEqual(self.give.__repr__(), rep)


class TestTake(unittest.TestCase):
    def setUp(self):
        self.ent_fact = entity_factory.EntityFactory()
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.player = self.ent_fact.new(objects.PLAYER)
        self.player.add(self.entity)

        self.evt_fact = event_factory.EventFactory()
        self.take = self.evt_fact.new(objects.TAKE)
        self.take.item_id = self.entity.spec.id
        self.take.new_owner = self.container

    def test_execute(self):
        self.assertIs(self.player.get(self.entity.spec.id), self.entity)
        self.take.execute(self.player)
        self.assertIs(self.player.get(self.entity.spec.id), None)
        self.assertIs(self.container.get(self.entity.spec.id), self.entity)

    def test_repr(self):
        rep = "<Take '{}'>".format(self.take.id)
        self.assertEqual(self.take.__repr__(), rep)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
