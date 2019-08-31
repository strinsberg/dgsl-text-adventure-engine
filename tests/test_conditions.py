import sys
import unittest
from unittest import mock
from io import StringIO
from contextlib import redirect_stdout
import dgsl_engine.conditions as conditions


class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.old_stdin = sys.stdin
        self.str_out = StringIO()
        self.question = conditions.Question('What is the secret code?', '1234')

    def tearDown(self):
        self.str_out.close()
        sys.stdin = self.old_stdin

    def test_right_answer(self):
        sys.stdin = StringIO('1234')

        with redirect_stdout(self.str_out):
            res = self.question.test(None)
            self.assertTrue(res)
            self.assertEqual(self.str_out.getvalue(),
                             "What is the secret code?\nAnswer: \n")
        sys.stdin.close()

    def test_wrong_answer(self):
        sys.stdin = StringIO('f4j8wf')
        res = self.question.test(None)
        self.assertFalse(res)
        sys.stdin.close()


class TestHasItem(unittest.TestCase):
    def setUp(self):
        self.container = mock.MagicMock()
        self.entity = mock.MagicMock()
        self.has_item = conditions.HasItem('SOMEID')

    def test_has_item(self):
        self.container.get.return_value = self.entity
        res = self.has_item.test(self.container)
        self.assertTrue(res)

    def test_no_item(self):
        self.container.get.return_value = None
        res = self.has_item.test(self.container)
        self.assertFalse(res)

    @mock.patch("dgsl_engine.collectors.EntityIdCollector")
    def test_has_item_other(self, collector):
        has_item = conditions.HasItem('SOMEID', mock.MagicMock(), mock.Mock())

        other = mock.MagicMock()
        other.get.return_value = self.entity
        collector.collect.return_value = other

        res = has_item.test(other)
        self.assertTrue(res)


class TestProtected(unittest.TestCase):
    def setUp(self):
        self.protected = conditions.Protected(['cold', 'wind'])
        self.hat = mock.MagicMock(protects=['cold', 'wind'], must_equip=True)
        self.cap = mock.MagicMock(protects=[])
        self.player = mock.MagicMock()
        # Can be lists because equipped and inventory are iterable
        self.player.equipped = []
        self.player.inventory = []

    def test_has_protection_equipped(self):
        self.player.equipped.append(self.hat)
        self.hat.equipped = True
        result = self.protected.test(self.player)
        self.assertTrue(result)

    @mock.patch('dgsl_engine.collectors.EntityTypeCollector')
    def test_has_protection_carrying(self, mock_collector):
        mock_collector.return_value.collect.return_value = [self.hat]
        self.hat.must_equip = False
        self.hat.equipped = False
        result = self.protected.test(self.player)
        self.assertTrue(result)

    @mock.patch('dgsl_engine.collectors.EntityTypeCollector')
    def test_no_protection(self, mock_collector):
        mock_collector.return_value.collect.return_value = [self.hat]
        self.hat.equipped = False
        self.player.equipped.append(self.cap)
        result = self.protected.test(self.player)
        self.assertFalse(result)
