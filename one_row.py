def one_row(game_from_db, players_db, response):
    players_db[game_from_db.id_p_now].stake_gap = game_from_db.highest_stake - players_db[
        game_from_db.id_p_now].stake

    if response == "fold":
        print(players_db[game_from_db.id_p_now].name + " fold")
        players_db[game_from_db.id_p_now].fold = True
        game_from_db.fold_list += players_db[game_from_db.id_p_now].name + " "
        if len(game_from_db.fold_list.split()) == (len(game_from_db.players.split()) - 1):
            for player_name in game_from_db.players.split():
                if player_name not in game_from_db.fold_list.split():
                    game_from_db.fold_out = True
                    game_from_db.winners += player_name
                    print(f"{player_name} выиграл, все - пас")
                    players_db[game_from_db.players.split().index(player_name)].win = True
                    game_from_db.round_ended = True
                    game_from_db.row = 4

    if response == "call":
        print(players_db[game_from_db.id_p_now].name + " call")
        players_db[game_from_db.id_p_now].stake += players_db[game_from_db.id_p_now].stake_gap
        game_from_db.pot += players_db[game_from_db.id_p_now].stake_gap
        players_db[game_from_db.id_p_now].chips -= players_db[game_from_db.id_p_now].stake_gap
        players_db[game_from_db.id_p_now].stake_gap = 0

    if response == "check" or players_db[game_from_db.id_p_now].all_in or \
            players_db[game_from_db.id_p_now].fold or game_from_db.fold_out:
        print(players_db[game_from_db.id_p_now].name + " check")

    if response == "all-in":
        players_db[game_from_db.id_p_now].stake += players_db[game_from_db.id_p_now].chips
        game_from_db.pot += players_db[game_from_db.id_p_now].chips
        game_from_db.highest_stake = players_db[game_from_db.id_p_now].stake
        players_db[game_from_db.id_p_now].stake_gap = 0
        players_db[game_from_db.id_p_now].chips = 0
        print(f"{players_db[game_from_db.id_p_now].name} ставит все!")
        players_db[game_from_db.id_p_now].all_in = True
        game_from_db.count_smth = 0
        game_from_db.all_in = True

    if response == "raise":
        print(f"Сколько {players_db[game_from_db.id_p_now].name} ставит? (доступно: "
              f"{players_db[game_from_db.id_p_now].chips})\n->")
        game_from_db.bet_ask = True

    if game_from_db.bet_ask:
        print("*Спрашиваем сколько ставит*")

    else:
        if game_from_db.count_smth == game_from_db.number_of_players:
            game_from_db.row += 1
            print("changed row on " + str(game_from_db.row))
        else:
            game_from_db.count_smth += 1
            game_from_db.id_p_now += 1
            game_from_db.id_p_now %= len(game_from_db.players.split())
            print("changed id_p_now on " + str(game_from_db.id_p_now))
            print("changed count_smth on " + str(game_from_db.count_smth))
            while players_db[game_from_db.id_p_now].fold or players_db[game_from_db.id_p_now].all_in:
                if game_from_db.count_smth == game_from_db.number_of_players:
                    game_from_db.row += 1
                    print("changed row on " + str(game_from_db.row))
                    break
                game_from_db.count_smth += 1
                game_from_db.id_p_now += 1
                game_from_db.id_p_now %= len(game_from_db.players.split())
                print("changed id_p_now on " + str(game_from_db.id_p_now))
                print("changed count_smth on " + str(game_from_db.count_smth))