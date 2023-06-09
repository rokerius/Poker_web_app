from bot_move import bot_move_1, bot_move_2
from game_info import give_game_info
from possible_responses import give_possible_responses


def one_row(game_from_db, players_db, response):
    players_db[game_from_db.id_p_now].stake_gap = game_from_db.highest_stake - players_db[
        game_from_db.id_p_now].stake

    if response == "check" or players_db[game_from_db.id_p_now].all_in or \
            players_db[game_from_db.id_p_now].fold or game_from_db.fold_out:
        players_db[game_from_db.id_p_now].stake_info = "CHECK"
        print(players_db[game_from_db.id_p_now].name + " check")

    if response == "fold":
        print(players_db[game_from_db.id_p_now].name + " fold")
        players_db[game_from_db.id_p_now].stake_info = "FOLD"
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
        if players_db[game_from_db.id_p_now].stake_info == "" or players_db[game_from_db.id_p_now].stake_info == "CHECK":
            players_db[game_from_db.id_p_now].stake_info = "CALL " + str(players_db[game_from_db.id_p_now].stake_gap)
        else:
            players_db[game_from_db.id_p_now].stake_info = "CALL " + \
                                                    str(players_db[game_from_db.id_p_now].stake_gap +
                                                        int(players_db[game_from_db.id_p_now].stake_info.split()[-1]))
        players_db[game_from_db.id_p_now].stake += players_db[game_from_db.id_p_now].stake_gap
        game_from_db.pot += players_db[game_from_db.id_p_now].stake_gap
        players_db[game_from_db.id_p_now].chips -= players_db[game_from_db.id_p_now].stake_gap
        players_db[game_from_db.id_p_now].stake_gap = 0

    if response == "all-in":
        if players_db[game_from_db.id_p_now].stake_info == "" or players_db[game_from_db.id_p_now].stake_info == "CHECK":
            players_db[game_from_db.id_p_now].stake_info = "ALL-IN " + str(players_db[game_from_db.id_p_now].chips)
        else:
            players_db[game_from_db.id_p_now].stake_info = "ALL-IN " + \
                                                    str(players_db[game_from_db.id_p_now].chips +
                                                        int(players_db[game_from_db.id_p_now].stake_info.split()[-1]))
        players_db[game_from_db.id_p_now].stake += players_db[game_from_db.id_p_now].chips
        game_from_db.pot += players_db[game_from_db.id_p_now].chips
        game_from_db.highest_stake = players_db[game_from_db.id_p_now].stake
        players_db[game_from_db.id_p_now].stake_gap = 0
        players_db[game_from_db.id_p_now].chips = 0
        print(f"{players_db[game_from_db.id_p_now].name} ставит все!")
        players_db[game_from_db.id_p_now].all_in = True
        game_from_db.count_smth = 0
        game_from_db.all_in = True

    if "raise" in response:
        if response == "raise":
            print(f"Сколько {players_db[game_from_db.id_p_now].name} ставит? (доступно: "
                f"{players_db[game_from_db.id_p_now].chips})\n->")
            game_from_db.bet_ask = True
        else:
            bet = int(response.split()[1])
            if bet > players_db[game_from_db.id_p_now].chips or bet <= 0 \
                    or bet < players_db[game_from_db.id_p_now].stake_gap:
                print("error: неверный ввод Бота, он не может столько поставить!")
            else:
                if bet == players_db[game_from_db.id_p_now].chips:
                    print(f"{players_db[game_from_db.id_p_now].name} ставит всё!")
                    players_db[game_from_db.id_p_now].all_in = True
                players_db[game_from_db.id_p_now].stake_gap = 0
                if players_db[game_from_db.id_p_now].stake_info == "" or \
                        players_db[game_from_db.id_p_now].stake_info == "CHECK":
                    players_db[game_from_db.id_p_now].stake_info = "RAISE " + str(bet)
                else:
                    players_db[game_from_db.id_p_now].stake_info = "RAISE " + str(bet +
                                                    int(players_db[game_from_db.id_p_now].stake_info.split()[-1]))
                players_db[game_from_db.id_p_now].stake += bet  # Вклад
                game_from_db.pot += bet  # Банк
                players_db[game_from_db.id_p_now].chips -= bet  # Фищки игрока
                game_from_db.highest_stake = players_db[game_from_db.id_p_now].stake
                game_from_db.count_smth = 2

    if game_from_db.bet_ask:
        print("*Спрашиваем сколько ставит*")

    else:
        if game_from_db.count_smth == game_from_db.number_of_players:
            game_from_db.row += 1
            print("changed row on " + str(game_from_db.row))
            for player in players_db:
                if player.stake_info != "FOLD":
                    player.stake_info = ""
        else:
            game_from_db.count_smth += 1
            game_from_db.id_p_now += 1
            game_from_db.id_p_now %= len(game_from_db.players.split())
            print("changed id_p_now on " + str(game_from_db.id_p_now))
            print("changed count_smth on " + str(game_from_db.count_smth))

            if players_db[game_from_db.id_p_now].bot:
                print("ХОДИТ БОТ")

                bot = players_db[game_from_db.id_p_now]
                game = give_game_info(game_from_db)
                give_possible_responses(players_db, game_from_db, game_from_db.id_p_now)
                if players_db[game_from_db.id_p_now].bot == 1:
                    response = bot_move_1(game, bot)
                    print("Ход Бота: " + response)
                else:
                    response = bot_move_2(game, bot)
                    print("Ход Бота: " + response)

                one_row(game_from_db, players_db, response)

            else:
                while players_db[game_from_db.id_p_now].fold or players_db[game_from_db.id_p_now].all_in:
                    if game_from_db.count_smth == game_from_db.number_of_players:
                        game_from_db.row += 1
                        print("changed row on " + str(game_from_db.row))
                        for player in players_db:
                            if player.stake_info != "FOLD":
                                player.stake_info = ""
                        break
                    game_from_db.count_smth += 1
                    game_from_db.id_p_now += 1
                    game_from_db.id_p_now %= len(game_from_db.players.split())
                    print("changed id_p_now on " + str(game_from_db.id_p_now))
                    print("changed count_smth on " + str(game_from_db.count_smth))

                    if players_db[game_from_db.id_p_now].bot:
                        print("ХОДИТ БОТ")

                        bot = players_db[game_from_db.id_p_now]
                        game = give_game_info(game_from_db)
                        give_possible_responses(players_db, game_from_db, game_from_db.id_p_now)
                        if players_db[game_from_db.id_p_now].bot == 1:
                            response = bot_move_1(game, bot)
                            print("Ход Бота: " + response)
                        else:
                            response = bot_move_2(game, bot)
                            print("Ход Бота: " + response)

                        one_row(game_from_db, players_db, response)