"""Game commands like quit and save."""
from . import user_input


def execute_command(verb, arg, game):
    """Executes a given command and return the result.

    Args:
      verb (str): The command to execute.
      arg (str): An argument to the command. Such as a name to save a
        game with.
      game (Game): The current game being played.

    Returns:
        str: The result of executing the command, Or some other message
            if the command does not exist (for now).

    """
    if verb in ['quit', 'exit']:
        return quit_game(game)
    return "Command " + str(arg)


def quit_game(game):
    """Confirms that the player wishes to quit the game and takes
    proper action.

    Args:
      game (Game): The game being played.

    Returns:
        str: A message about the result of the command.
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
