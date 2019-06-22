def execute_command(verb, arg, game):
    if verb in ['quit', 'exit']:
        return _quit(game)
    return "Command", True


def _quit(game):
    # eventually offer to save game
    return "Quitting ...", False