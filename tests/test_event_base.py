import unittest
from unittest import mock
import dgsl_engine.event_base as event_base
import dgsl_engine.entity_base as entity_base
import dgsl_engine.entity_containers as containers
import dgsl_engine.event_factory as event_factory
import dgsl_engine.entity_factory as entity_factory
from . import fakes
from . import json_objects as objects

# Should change to use the factories and json_objs sometime?
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

    def test_execute_is_done(self):
        self.event.is_done = True
        self.assertEqual(self.event.execute(None), '')

    def test_visit(self):
        visitor = fakes.FakeEventVisitor()
        self.event.accept(visitor)
        self.assertEqual(visitor.result, ID)

    def test_register(self):
        self.event.register(self.other_event)
        self.assertIn(self.other_event, self.event.subjects)

    def test_repr(self):
        rep = "<Event '{}'>".format(self.event.id)
        self.assertEqual(self.event.__repr__(), rep)


# Transfers ############################################################

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

    def test_execute_enter(self):
        self.container.add(self.entity)
        event = event_base.Event('3902483')
        event.message = 'Welcome to the room!'
        self.room.events.add('enter', event)
        self.room.spec.description = "You are in a ravine"
        self.entity.spec.name = 'a silver ring'

        self.move.destination = self.room
        self.move.message = 'You have moved to a new location.'
        result = self.move.execute(self.entity)
        self.assertEqual(
            result, ('You have moved to a new location.\n\n'
                     "You are in a ravine\n\nThere is ...\n   a silver ring\n\n"
                     'Welcome to the room!'))

    def test_execute_raises(self):
        self.room.add(self.player)
        self.move.destination = self.container
        with self.assertRaises(containers.ContainerError):
            self.move.execute(self.player)
        self.assertTrue(self.room.inventory.has_item(ID3))
        self.assertFalse(self.container.inventory.has_item(ID3))

    def test_visit(self):
        visitor = fakes.FakeEventVisitor()
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
        self.give.item_owner = self.container

    def test_execute(self):
        self.assertIs(self.container.get(self.entity.spec.id), self.entity)
        self.give.execute(self.player)
        self.assertIs(self.container.get(self.entity.spec.id), None)
        self.assertIs(self.player.get(self.entity.spec.id), self.entity)

    def test_accept(self):
        visitor = fakes.FakeEventVisitor()
        self.give.accept(visitor)
        self.assertEqual(visitor.result, self.give.id)

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

    def test_accept(self):
        visitor = fakes.FakeEventVisitor()
        self.take.accept(visitor)
        self.assertEqual(visitor.result, self.take.id)

    def test_repr(self):
        rep = "<Take '{}'>".format(self.take.id)
        self.assertEqual(self.take.__repr__(), rep)


# Toggles ##############################################################

class TestToggleActive(unittest.TestCase):
    def setUp(self):
        self.ent_fact = entity_factory.EntityFactory()
        self.entity = self.ent_fact.new(objects.ENTITY)

        self.evt_fact = event_factory.EventFactory()
        self.event = self.evt_fact.new(objects.TOGGLE_ACTIVE)
        self.event.target = self.entity

    def test_execute(self):
        self.assertTrue(self.entity.states.active)
        self.event.execute(None)
        self.assertFalse(self.entity.states.active)
        self.event.execute(None)
        self.assertTrue(self.entity.states.active)

    def test_execute_only_once(self):
        self.event.only_once = True
        self.assertTrue(self.entity.states.active)
        self.event.execute(None)
        self.assertFalse(self.entity.states.active)
        self.event.execute(None)
        self.assertFalse(self.entity.states.active)

    def test_accept(self):
        visitor = fakes.FakeEventVisitor()
        self.event.accept(visitor)
        self.assertEqual(visitor.result, self.event.id)

    def test_repr(self):
        rep = "<ToggleActive '{}'>".format(self.event.id)
        self.assertEqual(repr(self.event), rep)


class TestToggleObtainable(unittest.TestCase):
    def setUp(self):
        self.ent_fact = entity_factory.EntityFactory()
        self.entity = self.ent_fact.new(objects.ENTITY)

        self.evt_fact = event_factory.EventFactory()
        self.event = self.evt_fact.new(objects.TOGGLE_OBTAINABLE)
        self.event.target = self.entity

    def test_execute(self):
        self.assertTrue(self.entity.states.obtainable)
        self.event.execute(None)
        self.assertFalse(self.entity.states.obtainable)

    def test_execute_is_done(self):
        self.event.is_done = True
        self.assertTrue(self.entity.states.obtainable)
        self.event.execute(None)
        self.assertTrue(self.entity.states.obtainable)

    def test_repr(self):
        rep = "<ToggleObtainable '{}'>".format(self.event.id)
        self.assertEqual(repr(self.event), rep)


class TestToggleHidden(unittest.TestCase):
    def setUp(self):
        self.ent_fact = entity_factory.EntityFactory()
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.player = self.ent_fact.new(objects.PLAYER)

        self.evt_fact = event_factory.EventFactory()
        self.event = self.evt_fact.new(objects.TOGGLE_HIDDEN)
        self.event.target = self.entity

    def test_execute(self):
        self.assertFalse(self.entity.states.hidden)
        self.event.execute(None)
        self.assertTrue(self.entity.states.hidden)

    def test_execute_is_done(self):
        self.event.is_done = True
        self.assertFalse(self.entity.states.hidden)
        self.event.execute(None)
        self.assertFalse(self.entity.states.hidden)

    def test_execute_on_affected(self):
        self.event.target = None
        self.assertFalse(self.player.states.hidden)
        self.event.execute(self.player)
        self.assertTrue(self.player.states.hidden)

    def test_repr(self):
        rep = "<ToggleHidden '{}'>".format(self.event.id)
        self.assertEqual(repr(self.event), rep)


class TestEndGame(unittest.TestCase):
    def setUp(self):
        self.player = mock.MagicMock()
        self.event = event_base.EndGame('2394028')

    @mock.patch('dgsl_engine.event_base.Event.execute')
    def test_execute(self, mock_execute):
        mock_execute.return_value = "Event message"
        result = self.event.execute(self.player)
        self.assertTrue(self.player.hidden)
        self.assertEqual(result, 'Event message')

    def test_repr(self):
        rep = "<EndGame '{}'>".format(self.event.id)
        self.assertEqual(repr(self.event), rep)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
