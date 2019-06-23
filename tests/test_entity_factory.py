import unittest
import dgsl_engine.entity_factory as factory
import dgsl_engine.exceptions as exceptions

OBJ = {
    'id': '1234',
    'name': 'test object',
    'description': 'a simple testing object',
    'active': 1,
    'obtainable': 1,
    'hidden': 0
}


class TestEntityFactory(unittest.TestCase):
    def setUp(self):
        self.fact = factory.EntityFactory()
        self.obj = OBJ

    def test_new_entity(self):
        self.obj['type'] = 'entity'
        entity = self.fact.new(self.obj)
        self.assertEqual(entity.spec.id, OBJ['id'])
        self.assertEqual(entity.spec.name, OBJ['name'])
        self.assertEqual(entity.spec.description, OBJ['description'])
        self.assertTrue(entity.states.active)
        self.assertTrue(entity.states.obtainable)
        self.assertFalse(entity.states.hidden)

    def test_new_container(self):
        self.obj['type'] = 'container'
        container = self.fact.new(self.obj)
        self.assertEqual(container.spec.id, OBJ['id'])

    def test_new_room(self):
        self.obj['type'] = 'room'
        room = self.fact.new(self.obj)
        self.assertEqual(room.spec.id, OBJ['id'])
        self.assertTrue(room.states.active)
        self.assertFalse(room.states.obtainable)
        self.assertFalse(room.states.hidden)

    def test_new_player(self):
        self.obj['type'] = 'player'
        player = self.fact.new(self.obj)
        self.assertEqual(player.spec.id, OBJ['id'])

    def test_bad_type_throws(self):
        self.obj['type'] = 'barbecue'
        with self.assertRaises(exceptions.InvalidParameterError):
            self.fact.new(self.obj)

    def test_unfinished_obj_throws(self):
        obj = {'id': 'm40c0', 'name': 'unfinished'}
        with self.assertRaises(exceptions.InvalidParameterError):
            self.fact.new(obj)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()