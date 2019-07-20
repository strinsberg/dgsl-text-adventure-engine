import unittest
import unittest.mock as mock
import dgsl_engine.entity_containers as container

# Constants ############################################################

ID = "1234"
ID2 = '590ddsf'


# Tests ################################################################

class TestContainer(unittest.TestCase):
    def setUp(self):
        self.container = container.Container(ID)
        self.entity = container.Container(ID2)

    def test_add_entity(self):
        self.assertTrue(self.container.add(self.entity))
        self.assertEqual(self.entity.owner, self.container)

    @mock.patch('dgsl_engine.collectors.EntityIdCollector')
    def test_get_item(self, mock_collector):
        mock_collector.return_value.collect.return_value = self.entity
        self.container.add(self.entity)
        result = self.container.get(self.entity.spec.id)
        self.assertTrue(mock_collector.called)
        self.assertIs(result, self.entity)

    def test_iter(self):
        self.container.add(self.entity)
        result = ""
        for item in self.container:
            result += item.spec.id
        self.assertEqual(result, ID2)

    def test_add_throws(self):
        player = container.Player(ID)
        room = container.Room(ID)
        with self.assertRaises(container.ContainerError):
            self.container.add(player)
        with self.assertRaises(container.ContainerError):
            self.container.add(room)

    def test_add_already_there(self):
        self.container.add(self.entity)
        self.assertFalse(self.container.add(self.entity))

    def test_describe(self):
        self.container.spec.description = 'a small golden box'
        self.entity.spec.name = 'a leather pouch'
        self.container.add(self.entity)
        self.assertEqual(self.container.describe(),
                         "a small golden box\nIt holds a leather pouch")

    def test_accept(self):
        visitor = mock.MagicMock()
        self.container.accept(visitor)
        visitor.visit_container.assert_called_with(self.container)

    def test_repr(self):
        self.container.spec.name = 'test container'
        self.entity.spec.name = 'test entity'
        rep = ("<Container '{}', Name: '{}', "
               "Contents: {{<Container '{}', Name: '{}', "
               "Contents: {{}}>}}>").format(
            self.container.spec.id, self.container.spec.name,
            self.entity.spec.id, self.entity.spec.name)
        self.container.add(self.entity)
        self.assertEqual(repr(self.container), rep)


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = container.Room(ID)
        self.other_room = container.Room(ID)
        self.entity = container.Container(ID2)

    def test_init(self):
        self.assertTrue(self.room.states.active)
        self.assertFalse(self.room.states.obtainable)
        self.assertFalse(self.room.states.hidden)

    def test_add_entity(self):
        self.assertTrue(self.room.add(self.entity))
        self.assertEqual(self.entity.owner, self.room)

    def test_add_throws(self):
        with self.assertRaises(container.ContainerError):
            self.room.add(self.other_room)

    def test_add_already_there(self):
        self.room.add(self.entity)
        self.assertFalse(self.room.add(self.entity))

    def test_accept(self):
        visitor = mock.MagicMock()
        self.room.accept(visitor)
        visitor.visit_room.assert_called_with(self.room)

    def test_repr(self):
        self.room.spec.name = 'test room'
        self.entity.spec.name = 'test entity'
        rep = ("<Room '{}', Name: '{}', "
               "Contents: {{<Container '{}', Name: '{}', "
               "Contents: {{}}>}}>").format(
            self.room.spec.id, self.room.spec.name,
            self.entity.spec.id, self.entity.spec.name)
        self.room.add(self.entity)
        self.assertEqual(repr(self.room), rep)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = container.Player(ID)
        self.entity = container.Container(ID2)
        self.player.add(self.entity)

    def test_accept(self):
        visitor = mock.MagicMock()
        self.player.accept(visitor)
        visitor.visit_player.assert_called_with(self.player)

    def test_repr(self):
        self.player.spec.name = 'test entity'
        self.entity.spec.name = 'test entity'
        rep = ("<Player '{}', Name: '{}', "
               "Contents: {{<Container '{}', Name: '{}', "
               "Contents: {{}}>}}>").format(
            self.player.spec.id, self.player.spec.name,
            self.entity.spec.id, self.entity.spec.name)
        self.player.add(self.entity)
        self.assertEqual(repr(self.player), rep)
    # Will add tests when more functionality is added to the player

    def test_character_describe(self):
        desc = "a very adventurous sort"
        self.player.spec.description = desc
        self.assertEqual(self.player.describe(), desc)


class TestNpc(unittest.TestCase):
    def setUp(self):
        self.npc = container.Npc(ID)
        self.entity = container.Container(ID)
        self.npc.add(self.entity)

    def test_accept(self):
        visitor = mock.MagicMock()
        self.npc.accept(visitor)
        visitor.visit_npc.assert_called_with(self.npc)

    def test_repr(self):
        rep = ("<Npc '{}', Name: '{}', "
               "Contents: {{<Container '{}', Name: '{}', "
               "Contents: {{}}>}}>").format(
            self.npc.spec.id, self.npc.spec.name,
            self.entity.spec.id, self.entity.spec.name)
        self.assertEqual(repr(self.npc), rep)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
