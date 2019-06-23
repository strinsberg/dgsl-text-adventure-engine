if __name__ == '__main__':
    from dgsl_engine.game_factory import GameFactory
    world_name = 'testing ground'
    game = GameFactory().new(world_name)
    game.run()
