import unittest
import dgsl_engine.user_input as user_input

INPUT = "get chocolate cake"


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = user_input.Parser()

    def test_parse(self):
        parsed = self.parser.parse(INPUT)
        self.assertEqual(parsed['verb'], "get")
        self.assertEqual(parsed['subject'], 'chocolate cake')


# Main #################################################################

if __name__ == '__main__':
    unittest.main()