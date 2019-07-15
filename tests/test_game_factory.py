import unittest
import dgsl_engine.game_factory as factory


# Tests ################################################################

class TestGameFactory(unittest.TestCase):
    def setUp(self):
        fact = factory.GameFactory()
        self.game = fact.new('testing_ground')

    def test_new(self):
        # Not really an adequate tests, but it runs the code.
        self.assertEqual(self.game.world.details.name, 'testing ground')
        self.assertEqual(self.game.world.details.version, '0.0')
        self.assertEqual(self.game.world.details.welcome, 'fun is waiting!')


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
