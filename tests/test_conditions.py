import unittest
import dgsl_engine.conditions as conditions
from dgsl_engine.entity_factory import EntityFactory
from . import json_objects as objects
from . import fakes


class TestQuestion(unittest.TestCase):
    def setUp(self):
        self._out = fakes.FakeOutput()
        self.question = conditions.Question('What is the secret code?', '1234')
        self.question._out = self._out.make_capture()

    def test_right_answer(self):
        in_ = fakes.FakeInput(['1234'])
        self.question._in = in_.make_stream()
        res = self.question.test(None)
        self.assertTrue(res)
        self.assertEqual(self._out.get_text(),
                         "What is the secret code?\n")

    def test_wrong_answer(self):
        in_ = fakes.FakeInput(['f4j8wf'])
        self.question._in = in_.make_stream()
        res = self.question.test(None)
        self.assertFalse(res)


class TestHasItem(unittest.TestCase):
    def setUp(self):
        self.fact = EntityFactory()
        self.container = self.fact.new(objects.CONTAINER)
        self.entity = self.fact.new(objects.ENTITY)
        self.has_item = conditions.HasItem(self.entity.spec.id)

    def test_has_item(self):
        self.container.add(self.entity)
        res = self.has_item.test(self.container)
        self.assertTrue(res)

    def test_no_item(self):
        res = self.has_item.test(self.container)
        self.assertFalse(res)


class TestProtected(unittest.TestCase):
    def setUp(self):
        self.protected = conditions.Protected(['cold', 'wind'])
        self.fact = EntityFactory()
        self.hat = self.fact.new(objects.EQUIPMENT)
        self.cap = self.fact.new(objects.EQUIPMENT2)
        self.player = self.fact.new(objects.PLAYER)

    def test_has_protection_equipped(self):
        self.player.equipped.equip(self.hat)
        result = self.protected.test(self.player)
        self.assertTrue(result)

    def test_has_protection_carrying(self):
        self.player.equipped.equip(self.cap)
        self.hat.must_equip = False
        self.player.add(self.hat)
        result = self.protected.test(self.player)
        self.assertTrue(result)

    def test_no_protection(self):
        self.player.equipped.equip(self.cap)
        self.player.add(self.hat)
        result = self.protected.test(self.player)
        self.assertFalse(result)
