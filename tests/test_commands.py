import unittest
import dgsl_engine.commands as commands

# Mocks ################################################################


class MockGame:
    # Expand or replace with real game when commands grow
    def __init__(self):
        pass


# Testing ##############################################################


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.game = MockGame()

    def test_temp_branch(self):
        message, status = commands.execute_command('any', None, self.game)
        self.assertEqual(message, 'Command')
        self.assertTrue(status)

    def test_quit(self):
        message, status = commands.execute_command('quit', None, self.game)
        self.assertEqual(message, 'Quitting ...')
        self.assertFalse(status)


# Main #################################################################

if __name__ == '__main__':
    unittest.main()