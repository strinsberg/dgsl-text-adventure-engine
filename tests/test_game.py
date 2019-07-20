import unittest
import dgsl_engine.game as game
import dgsl_engine.world as world
import dgsl_engine.user_input as user_input
from dgsl_engine.entity_containers import Player, Room
from . import fakes

input_text = ['get test entity', 'drop test entity', 'dance', 'quit']
results = ['You get entity', 'You drop entity', "You don't know how to dance"]
other_results = ['Quitting ...\n', 'Thanks for playing']


class TestGame(unittest.TestCase):
    def setUp(self):
        self.output = fakes.FakeOutput()
        self.input = fakes.FakeInput(input_text)
        self.world = world.World()
        self.world.player = Player('id')
        self.world.player.owner = Room('u0s9uf')
        self.parser = user_input.Parser()
        self.resolver = fakes.FakeResolver(results)
        self.game = game.Game(self.world, self.parser, self.resolver)
        self.game._out = self.output.make_capture()
        self.game._in = self.input.make_stream()
        self.maxDiff = None

    def test_run(self):
        self.game.run()
        out = self.output.get_text()
        expected_out = (
            '\n----------------------------------------------------\n'
            'Null\n')
        for output in results:
            expected_out += (
                "\n----------------------------------------------------\n" +
                output + '\n')
        expected_out += "\n----------------------------------------------------\n"
        self.assertEqual(out, expected_out + "\n".join(other_results) + '\n')


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
