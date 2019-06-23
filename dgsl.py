if __name__ == '__main__':
    import os
    import json
    import dgsl_engine.game as game
    import dgsl_engine.user_input as user_input
    import dgsl_engine.world as world
    import dgsl_engine.actions as actions
    import dgsl_engine.visitors as visitors

    parser = user_input.Parser()

    collector_factory = visitors.EntityCollectorFactory()
    menu_factory = user_input.MenuFactory()
    action_factory = actions.ActionFactory()
    resolver = actions.ActionResolver(collector_factory, menu_factory,
                                      action_factory)

    world_path = "testing_ground.world"
    home = os.path.expanduser('~')
    path = os.path.join(home, ".dgsl/worlds", world_path)

    with open(path) as file:
        world_json = json.load(file)

    game_world = world.WorldFactory().new(world_json)

    new_game = game.Game(game_world, parser, resolver)
    new_game.run()
