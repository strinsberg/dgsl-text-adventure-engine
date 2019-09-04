import unittest
import unittest.mock as mock
import dgsl_engine.commands as commands

# Mocks ################################################################


class MockGame:
    # Expand or replace with real game when commands grow
    def __init__(self):
        self.end = False


# Testing ##############################################################


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.game = MockGame()

    def test_temp_branch(self):
        message = commands.execute_command('any', 'None', self.game)
        self.assertEqual(message, 'Command None')

    @mock.patch('dgsl_engine.user_input.Menu')
    def test_quit(self, mock_menu):
        mock_menu.return_value.ask.return_value = 0
        message = commands.execute_command('quit', None, self.game)
        self.assertEqual(message, '\nQuitting ...')
        self.assertTrue(self.game.end)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()
