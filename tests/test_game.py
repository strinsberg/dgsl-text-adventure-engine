import unittest
import dgsl_engine.game as game
import dgsl_engine.world as world
import dgsl_engine.user_input as user_input
from dgsl_engine.entity_containers import Player
from . import fakes

input_text = ['get test entity', 'drop test entity', 'dance', 'quit']
results = ['You get entity', 'You drop entity', "You don't know how to dance"]
other_results = ['Quitting ...', 'Thanks for playing']


class TestGame(unittest.TestCase):
    def setUp(self):
        self.output = fakes.FakeOutput()
        self.input = fakes.FakeInput(input_text)
        self.world = world.World()
        self.world.player = Player('id')
        self.parser = user_input.Parser()
        self.resolver = fakes.FakeResolver(results)
        self.game = game.Game(self.world, self.parser, self.resolver,
                              self.output.make_capture(),
                              self.input.make_stream())

    def test_run(self):
        self.game.run()
        out = self.output.get_text()
        expected_out = ''
        for output in results:
            expected_out += (
                "\n----------------------------------------------------" +
                output)
        expected_out += "\n----------------------------------------------------"
        self.assertEqual(out, expected_out + "".join(other_results))


# Main #################################################################

if __name__ == '__main__':
    unittest.main()