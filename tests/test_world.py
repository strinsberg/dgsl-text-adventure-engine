import unittest
import os
import json
import dgsl_engine.world as world

test_world_path = 'tests/worlds/testing_ground.world'


class TestWorld(unittest.TestCase):
    pass


class TestWorldFactory(unittest.TestCase):
    def setUp(self):
        with open(test_world_path) as file:
            self.world_json = json.load(file)
        self.world_fact = world.WorldFactory()

    def test_create_objects(self):
        new_world = world.World()
        self.world_fact._create_objects(new_world, self.world_json)
        for id_, obj in self.world_json['objects'].items():
            if world.is_entity(obj):
                self.assertIn(id_, new_world.entities)
            elif world.is_event(obj):
                self.assertIn(id_, new_world.events)
        # Not sure this confirms that actual entities were created. just that
        # something was added with their id

    def test_connect_objects(self):
        new_world = world.World()
        self.world_fact._create_objects(new_world, self.world_json)
        self.world_fact._connect_objects(new_world, self.world_json)

        # Can only realy test a few based on knowledge of the test world
        # Ring in room
        capt_room = new_world.entities['53b33006-f98c-430e-aee0-53002171c8b8']
        ring = new_world.entities['78ad7618-75fc-4294-98fa-139a0434c723']
        self.assertIs(ring, capt_room.inventory.items[ring.spec.id])

        # Door to common room has use event to move to common room
        door_to_common = new_world.entities[
            'eace0959-3266-42ce-a70a-c8179c508d36']
        to_common = new_world.events['644a31eb-8896-43c3-9ad1-5ab1ae5b210a']
        self.assertIs(to_common, door_to_common.events.events['use'])

        # Player is in captains room to start
        player = new_world.entities['player']
        self.assertIs(player, capt_room.inventory.items[player.spec.id])

    def test_new_world(self):
        new_world = self.world_fact.new(self.world_json)

        # Just confirm some objects were created and connected
        player = new_world.entities['player']
        capt_room = new_world.entities['53b33006-f98c-430e-aee0-53002171c8b8']
        self.assertIs(player, capt_room.inventory.items[player.spec.id])

        # Check to see world details are setup properly
        self.assertIs(player, new_world.player)
        self.assertEqual(new_world.name, 'testing ground')
        self.assertEqual(new_world.version, '0.0')
        self.assertEqual(new_world.welcome, 'fun is waiting!')


# Main #################################################################

if __name__ == '__main__':
    unittest.main()