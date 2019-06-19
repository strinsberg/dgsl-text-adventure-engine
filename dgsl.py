if __name__ == '__main__':
    import dgsl_engine.game as game
    import dgsl_engine.user_input as user_input

    parser = user_input.Parser()
    game.Game(parser).run()