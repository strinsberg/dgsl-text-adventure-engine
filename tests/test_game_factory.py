import unittest
import dgsl_engine.game_factory as factory


# Tests ################################################################

class TestGameFactory(unittest.TestCase):
    def setUp(self):
        fact = factory.GameFactory()
        self.game = fact.new('tests/worlds/testing_ground')

    def test_new(self):
        # Not really an adequate tests, but it runs the code.
        self.assertEqual(self.game.world.details.name, 'testing ground')
        self.assertEqual(self.game.world.details.version, '0.0')
        self.assertEqual(self.game.world.details.welcome, 'fun is waiting!')

    def test_name_to_path(self):
        name = 'some fun world'
        path = 'some_fun_world.world'
        self.assertEqual(factory.name_to_path(name), path)

# Main #################################################################


if __name__ == '__main__':
    unittest.main()
