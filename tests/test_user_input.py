import unittest
import dgsl_engine.user_input as user_input

INPUT = "get chocolate cake"

# Mocks ################################################################


class MockOutput:
    def __init__(self):
        self.text = []

    def make_capture(self):
        return lambda text: self.text.append(text)

    def get_text(self):
        return "".join(self.text)


# Testing ##############################################################


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = user_input.Parser()

    def test_parse(self):
        parsed = self.parser.parse(INPUT)
        self.assertEqual(parsed['verb'], "get")
        self.assertEqual(parsed['object'], 'chocolate cake')

    def test_command(self):
        parsed = self.parser.parse('quit')
        self.assertEqual(parsed['code'], user_input.ParseCodes.COMMAND)

    def test_not_valid_verb(self):
        parsed = self.parser.parse('crump')
        self.assertEqual(parsed['code'], user_input.ParseCodes.BAD_VERB)
        self.assertEqual(parsed['message'], "You don't know how to crump")


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.choices = ["climb the cliff", "eat the bagel", "jump around"]
        self.out = MockOutput()
        self.menu = user_input.Menu(self.choices, self.out.make_capture())

    def test_ask(self):
        idx = self.menu.ask(['1'])
        self.assertEqual(idx, 1)
        self.assertEqual(
            self.out.get_text(), "1. climb the cliff\n"
            "2. eat the bagel\n"
            "3. jump around\n"
            "4. Cancel\n")


# Main #################################################################

if __name__ == '__main__':
    unittest.main()