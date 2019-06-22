import unittest
import dgsl_engine.actions as actions
import dgsl_engine.game as game
import dgsl_engine.entity_containers as containers
import dgsl_engine.entity_base as entity
import dgsl_engine.event_base as event_base
import dgsl_engine.event_single_decorators as decorators

ID = "223084"
P_ID = "1234"
ROOM_ID = "5678"
CONT_ID = "6543"
ENT_ID = "04938"
ENT_NAME = "a golden ring"
CONT_NAME = "an old wooden box"
MESSAGE = "You feel cursed!"


# Eventually this should be split up to test each action seperately
# Also eventually updated with factories so that it is easy to get certain
# entities and events without all this typing.
class TestActions(unittest.TestCase):
    def setUp(self):
        self.world = game.World()
        self.world.player = containers.Player(P_ID)
        self.room = containers.Room(ROOM_ID)
        self.entity = entity.Entity(ENT_ID)
        self.container = containers.Container(CONT_ID)

        self.entity.spec.name = ENT_NAME
        self.container.spec.name = CONT_NAME

        self.room.add(self.container)
        self.room.add(self.world.player)
        self.container.add(self.entity)

        self.event = decorators.MessageDecorator(event_base.Event(ID), MESSAGE)

        self.world.entities[ROOM_ID] = self.room

    def test_get_obtainable(self):
        result = actions._take_action('get', self.container, None, self.world)
        self.assertFalse(self.room.inventory.has_item(CONT_ID))
        self.assertTrue(self.world.player.inventory.has_item(CONT_ID))
        self.assertEqual(result, "You take " + CONT_NAME)

    def test_get_not_obtainable(self):
        self.container.states.obtainable = False
        result = actions._take_action('get', self.container, None, self.world)
        self.assertTrue(self.room.inventory.has_item(CONT_ID))
        self.assertFalse(self.world.player.inventory.has_item(CONT_ID))
        self.assertEqual(result, "You can't take that")

    def test_use_ring_no_event(self):
        result = actions._take_action('use', self.entity, None, self.world)
        self.assertEqual(result, "You can't use that")

    def test_use_ring_has_event(self):
        self.entity.events.add('use', self.event)
        result = actions._take_action('use', self.entity, None, self.world)
        self.assertEqual(result, "You use {}\n{}".format(ENT_NAME, MESSAGE))


class TestActionResolver(unittest.TestCase):
    pass


# Main #################################################################

if __name__ == '__main__':
    unittest.main()