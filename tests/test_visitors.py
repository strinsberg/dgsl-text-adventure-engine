import unittest
import dgsl_engine.visitors as visitor
from dgsl_engine.entity_factory import EntityFactory
from dgsl_engine.event_factory import EventFactory
from dgsl_engine.world import World
from . import json_objects as objects


class TestEntityCollector(unittest.TestCase):
    def setUp(self):
        self.ent_fact = EntityFactory()
        self.room = self.ent_fact.new(objects.ROOM)
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.equipment = self.ent_fact.new(objects.EQUIPMENT)
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

    def test_visit_npc_for_npc(self):
        npc = self.ent_fact.new(objects.NPC)
        npc.add(self.entity)
        self.room.add(npc)
        collector = visitor.EntityCollector('pauline', None, self.room)
        entities = collector.collect()
        self.assertIs(entities[0], npc)

    def test_visit_npc_for_contents(self):
        npc = self.ent_fact.new(objects.NPC)
        npc.add(self.entity)
        self.room.add(npc)
        self.room.inventory.remove(self.entity.spec.id)
        collector = visitor.EntityCollector('test', None, self.room)
        entities = collector.collect()
        self.assertNotIn(self.entity, entities)

    def test_visit_npc_for_equipment(self):
        npc = self.ent_fact.new(objects.NPC)
        npc.equipped.equip(self.equipment)
        self.room.add(npc)
        self.room.inventory.remove(self.entity.spec.id)
        collector = visitor.EntityCollector('hat', None, self.room)
        entities = collector.collect()
        self.assertNotIn(self.equipment, entities)

    def test_visit_player_for_player(self):
        player = self.ent_fact.new(objects.PLAYER)
        player.add(self.entity)
        self.room.add(player)
        collector = visitor.EntityCollector('test player', None, self.room)
        entities = collector.collect()
        self.assertIs(entities[0], player)

    def test_visit_player_for_equipment(self):
        player = self.ent_fact.new(objects.PLAYER)
        player.equipped.equip(self.equipment)
        self.room.add(player)
        collector = visitor.EntityCollector('hat', None, self.room)
        entities = collector.collect()
        self.assertIs(entities[0], self.equipment)

    # Add visit specific functions when you start adding more
    # If the factory ever gets ore complex then add it's own test


class TestEntityTypeCollector(unittest.TestCase):
    def setUp(self):
        self.fact = EntityFactory()
        self.entity = self.fact.new(objects.ENTITY)
        self.container = self.fact.new(objects.CONTAINER)
        self.player = self.fact.new(objects.PLAYER)
        self.npc = self.fact.new(objects.NPC)
        self.room = self.fact.new(objects.ROOM)
        self.equipment = self.fact.new(objects.EQUIPMENT)
        self.container.add(self.entity)
        self.player.add(self.container)
        self.room.add(self.player)
        self.room.add(self.npc)
        self.player.equipped.equip(self.equipment)

    def test_collect_entity(self):
        self.collector = visitor.EntityTypeCollector(
            ['entity'], self.container)
        self.collector.collect()
        self.assertIn(self.entity, self.collector.results)
        self.assertEqual(len(self.collector.results), 1)

    def test_collect_container(self):
        self.collector = visitor.EntityTypeCollector(['container'], self.room)
        self.collector.collect()
        self.assertIn(self.container, self.collector.results)
        self.assertEqual(len(self.collector.results), 1)

    def test_collect_player(self):
        self.collector = visitor.EntityTypeCollector(['player'], self.room)
        self.collector.collect()
        self.assertIn(self.player, self.collector.results)
        self.assertEqual(len(self.collector.results), 1)

    def test_collect_npc(self):
        self.collector = visitor.EntityTypeCollector(['npc'], self.room)
        self.collector.collect()
        self.assertIn(self.npc, self.collector.results)
        self.assertEqual(len(self.collector.results), 1)

    def test_collect_equipment(self):
        self.collector = visitor.EntityTypeCollector(['equipment'], self.room)
        self.collector.collect()
        self.assertIn(self.equipment, self.collector.results)
        self.assertEqual(len(self.collector.results), 1)

    def test_collect_room(self):
        self.collector = visitor.EntityTypeCollector(['room'], self.room)
        self.collector.collect()
        self.assertIn(self.room, self.collector.results)
        self.assertEqual(len(self.collector.results), 1)


class TestEntityConnector(unittest.TestCase):
    def setUp(self):
        self.ent_fact = EntityFactory()
        self.evt_fact = EventFactory()
        self.json_objs = [
            objects.ENTITY, objects.CONTAINER, objects.PLAYER, objects.ROOM
        ]
        self.world = World()
        self.entity = self.ent_fact.new(objects.ENTITY)
        self.container = self.ent_fact.new(objects.CONTAINER)
        self.player = self.ent_fact.new(objects.PLAYER)
        self.npc = self.ent_fact.new(objects.NPC)
        self.room = self.ent_fact.new(objects.ROOM)
        self.world.add_entity(self.entity)
        self.world.add_entity(self.container)
        self.world.add_entity(self.room)
        self.world.add_entity(self.player)
        self.world.add_entity(self.npc)
        self.world.add_event(self.evt_fact.new(objects.INFORM))

    def test_connect_entity(self):
        connector = visitor.EntityConnector(objects.ENTITY, self.world)
        connector.connect(self.entity)
        self.assertTrue(self.entity.events.has_event('use'))

    def test_connect_container(self):
        connector = visitor.EntityConnector(objects.ROOM, self.world)
        connector.connect(self.room)
        self.assertTrue(self.room.events.has_event('use'))
        self.assertTrue(self.room.inventory.has_item(self.entity.spec.id))
        self.assertTrue(self.room.inventory.has_item(self.player.spec.id))
        self.assertTrue(self.room.inventory.has_item(self.npc.spec.id))
        self.assertTrue(self.room.inventory.has_item(self.container.spec.id))

    def test_connect_player(self):
        connector = visitor.EntityConnector(objects.PLAYER, self.world)
        connector.connect(self.player)
        self.assertTrue(self.player.events.has_event('use'))

    def test_connect_npc(self):
        connector = visitor.EntityConnector(objects.NPC, self.world)
        connector.connect(self.npc)
        self.assertTrue(self.npc.events.has_event('use'))


class TestEventConnector(unittest.TestCase):
    def setUp(self):
        self.evt_fact = EventFactory()
        self.event = self.evt_fact.new(objects.EVENT)
        self.inform = self.evt_fact.new(objects.INFORM)
        self.move = self.evt_fact.new(objects.MOVE)
        self.ent_fact = EntityFactory()
        self.room = self.ent_fact.new(objects.ROOM)
        self.world = World()
        self.world.add_event(self.event)
        self.world.add_event(self.inform)
        self.world.add_event(self.move)
        self.world.add_entity(self.room)

    def test_connect_event(self):
        connector = visitor.EventConnector(objects.INFORM, self.world)
        connector.connect(self.inform)
        self.assertIn(self.event, self.inform.subjects)

    def test_connect_move(self):
        connector = visitor.EventConnector(objects.MOVE, self.world)
        connector.connect(self.move)
        self.assertIn(self.inform, self.move.subjects)
        self.assertIs(self.move.destination, self.room)

    def test_connect_give(self):
        give = self.evt_fact.new(objects.GIVE)
        cont = self.ent_fact.new(objects.NPC)
        self.world.add_entity(cont)
        connector = visitor.EventConnector(objects.GIVE, self.world)
        connector.connect(give)
        self.assertEqual(give.item_owner, cont)

    def test_connect_take(self):
        take = self.evt_fact.new(objects.TAKE)
        cont = self.ent_fact.new(objects.NPC)
        self.world.add_entity(cont)
        connector = visitor.EventConnector(objects.TAKE, self.world)
        connector.connect(take)
        self.assertEqual(take.new_owner, cont)

    def test_connect_toggle(self):
        toggle = self.evt_fact.new(objects.TOGGLE_ACTIVE)
        cont = self.ent_fact.new(objects.NPC)
        self.world.add_entity(cont)
        connector = visitor.EventConnector(objects.TOGGLE_ACTIVE, self.world)
        connector.connect(toggle)
        self.assertEqual(toggle.target, cont)

    def test_connect_group(self):
        group = self.evt_fact.new(objects.GROUP)
        connector = visitor.EventConnector(objects.GROUP, self.world)
        connector.connect(group)
        self.assertIn(self.event, group.events)
        self.assertIn(self.inform, group.events)

    def test_connect_conditional(self):
        pass

    def test_connect_interaction(self):
        pass

# Main #################################################################


if __name__ == '__main__':
    unittest.main()
