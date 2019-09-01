"""Game commands like quit and save."""
from . import user_input


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
    return "Command " + str(arg)


def _quit(game):
    """

    Args:
      game:

    Returns:

    """
    menu = user_input.Menu(['Save and Quit (not implemented)', 'Quit'])
    answer = menu.ask()

    result = "Quitting ..."

    if answer == 0:
        # save game here. add game save logic to the result before returning
        game.end = True
    elif answer == 1:
        game.end = True
    else:
        result = "Cancelled"

    return result
