import unittest
import unittest.mock as mock
import dgsl_engine.event_factory as factory
import dgsl_engine.exceptions as exceptions
from . import json_objects

OBJ = {'id': '1234', 'once': 1, 'item': {'id': 'none'}}


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
        self.obj['item']['id'] = 'none'
        event = self.fact.new(self.obj)
        self.assertEqual(event.id, OBJ['id'])

    def test_new_take(self):
        self.obj['type'] = 'take'
        self.obj['item']['id'] = 'none'
        event = self.fact.new(self.obj)
        self.assertEqual(event.id, OBJ['id'])

    def test_new_unfinished_object_throws(self):
        with self.assertRaises(exceptions.InvalidParameterError):
            self.fact.new({'id': '09r8320'})

    def test_new_invalid_type(self):
        with self.assertRaises(exceptions.InvalidParameterError):
            self.obj['type'] = 'not_real'
            self.fact.new(self.obj)


class TestMakeCondition(unittest.TestCase):
    def test_make_has_item(self):
        has_item = factory.make_condition(json_objects.HAS_ITEM)
        self.assertEqual(has_item.item_id, json_objects.HAS_ITEM['item']['id'])

    def test_make_question(self):
        question = factory.make_condition(json_objects.QUESTION)
        q = json_objects.QUESTION['question']
        a = json_objects.QUESTION['answer']
        self.assertEqual(question.question, q)
        self.assertEqual(question.answer, a)

    def test_make_protected(self):
        protected = factory.make_condition(json_objects.PROTECTED)
        self.assertEqual(protected.effects, json_objects.PROTECTED['effects'])

    def test_incomplete_json(self):
        obj = {}
        with self.assertRaises(exceptions.InvalidParameterError):
            factory.make_condition(obj)

    def test_bad_type(self):
        obj = {'type': 'camel'}
        with self.assertRaises(exceptions.InvalidParameterError):
            factory.make_condition(obj)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
