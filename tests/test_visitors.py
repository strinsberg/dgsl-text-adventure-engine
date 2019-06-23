import unittest
import dgsl_engine.visitors as visitor
import dgsl_engine.entity_factory as ent_fact
import dgsl_engine.event_factory as evt_fact
import dgsl_engine.game as game
from . import json_objects as objects


class TestEntityCollector(unittest.TestCase):
    def setUp(self):
        self.ent_fact = ent_fact.EntityFactory()
        self.room = self.ent_fact.new(objects.ROOM)
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.room.add(self.entity)
        self.room.add(self.container)

    def test_collect_no_results(self):
        fact = visitor.EntityCollectorFactory()
        collector = fact.make('never find it', None, self.room)
        entities = collector.collect()
        self.assertFalse(entities)

    def test_collect_one_result(self):
        collector = visitor.EntityCollector('test entity', None, self.room)
        entities = collector.collect()
        self.assertIs(entities[0], self.entity)

    def test_collect_many_results(self):
        collector = visitor.EntityCollector('test', None, self.room)
        entities = collector.collect()
        self.assertEqual(len(entities), len(self.room.inventory.items))
        for entity in entities:
            self.assertTrue(self.room.inventory.has_item(entity.spec.id))

    # Add visit specific functions when you start adding more
    # If the factory ever gets ore complex then add it's own test


class TestEntityConnector(unittest.TestCase):
    def setUp(self):
        self.ent_fact = ent_fact.EntityFactory()
        self.evt_fact = evt_fact.EventFactory()
        self.json_objs = [
            objects.ENTITY, objects.CONTAINER, objects.PLAYER, objects.ROOM
        ]
        self.world = game.World()
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.player = self.ent_fact.new(objects.PLAYER)
        self.room = self.ent_fact.new(objects.ROOM)
        self.world.add_entity(self.entity)
        self.world.add_entity(self.container)
        self.world.add_entity(self.room)
        self.world.add_entity(self.player)
        self.world.add_event(self.evt_fact.new(objects.INFORM))

    def test_connect_entity(self):
        print(self.world.entities)
        connector = visitor.EntityConnector(objects.ENTITY, self.world)
        connector.connect(self.entity)
        self.assertTrue(self.entity.events.has_event('use'))

    def test_connect_container(self):
        connector = visitor.EntityConnector(objects.ROOM, self.world)
        connector.connect(self.room)
        self.assertTrue(self.room.events.has_event('use'))
        self.assertTrue(self.room.inventory.has_item(self.entity.spec.id))
        self.assertTrue(self.room.inventory.has_item(self.player.spec.id))
        self.assertTrue(self.room.inventory.has_item(self.container.spec.id))


class TestEventConnector(unittest.TestCase):
    pass


# Main #################################################################

if __name__ == '__main__':
    unittest.main()