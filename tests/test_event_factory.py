import unittest
import dgsl_engine.event_factory as factory
import dgsl_engine.exceptions as exceptions

OBJ = {'id': '1234', 'once': 1}


class TestEventFactory(unittest.TestCase):
    def setUp(self):
        self.fact = factory.EventFactory()
        self.obj = OBJ

    def test_new_event(self):
        self.obj['type'] = 'event'
        event = self.fact.new(self.obj)
        self.assertEqual(event.id, OBJ['id'])
        self.assertFalse(event.is_done)
        self.assertTrue(event.only_once)

    def test_new_move(self):
        self.obj['type'] = 'move'
        event = self.fact.new(self.obj)
        self.assertEqual(event.id, OBJ['id'])

    def test_new_give(self):
        self.obj['type'] = 'give'
        event = self.fact.new(self.obj)
        self.assertEqual(event.id, OBJ['id'])

    def test_new_take(self):
        self.obj['type'] = 'take'
        event = self.fact.new(self.obj)
        self.assertEqual(event.id, OBJ['id'])

    def test_new_unfinished_object_throws(self):
        with self.assertRaises(exceptions.InvalidParameterError):
            self.fact.new({'id': '09r8320'})

    def test_new_invalid_type(self):
        with self.assertRaises(exceptions.InvalidParameterError):
            self.obj['type'] = 'not_real'
            self.fact.new(self.obj)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
