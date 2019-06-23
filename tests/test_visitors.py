import unittest
import dgsl_engine.visitors as visitor
import dgsl_engine.entity_factory as ent_fact
import dgsl_engine.game as game
from . import objects


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


class TestEntityCollectorFactory(unittest.TestCase):
    pass


class TestEntityConnector(unittest.TestCase):
    pass


class TestEventConnector(unittest.TestCase):
    pass


class TestEventConnectorFactory(unittest.TestCase):
    pass


# Main #################################################################

if __name__ == '__main__':
    unittest.main()