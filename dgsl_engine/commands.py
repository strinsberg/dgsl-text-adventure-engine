"""Game commands like quit and save."""


def execute_command(verb, arg, game):
    """

    Args:
      verb:
      arg:
      game:

    Returns:

    """
    if verb in ['quit', 'exit']:
        return _quit(game)
    return "Command", True


def _quit(game):
    """

    Args:
      game:

    Returns:

    """
    # eventually offer to save game
    return "Quitting ...", False
