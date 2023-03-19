from the_game_class import Game


def startgame(game):
    game.deck.shuffle()
    game.give_player_attributes()

    game.deal_razdacha()
    game.print_round_info()

    game.act_one()
    game.print_round_info()

    if not game.round_ended:
        game.deal_flop()
        game.print_round_info()
    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
    if not game.round_ended:
        game.deal_turn()
        game.print_round_info()
    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
    if not game.round_ended:
        game.deal_river()
        game.print_round_info()
    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
    if not game.round_ended:
        game.score_all()
        game.print_round_info()

    game.find_winners()

    game.print_round_info()
    game.round_ended = True
    print(game.winners, game.winner, [player for player in game.list_of_players_not_out if player.win])
    game.end_round()


game1 = Game()
while True:
    startgame(game1)
