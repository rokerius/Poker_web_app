def find_winner(game_from_db, players_db):
    if game_from_db.fold_out:
        for player in game_from_db.winners.split():
            coosh = int((game_from_db.pot / len(game_from_db.winners.split())))
            players_db[game_from_db.players.split().index(player)].chips += coosh
            print(f"{players_db[game_from_db.players.split().index(player)].name} выиграл {coosh} фишек!")
    else:
        list_of_stakes = []
        for player in players_db:
            if not player.fold:
                list_of_stakes.append(player.score.split())
        max_score = max(list_of_stakes)  # это мы нашли максимальное колличество очков
        for player in players_db:
            if player.score.split() == max_score \
                    and not player.fold:
                print(player.name + "выиграл")
                player.win = True
                player.k_wins = int(player.k_wins) + 1
                game_from_db.winners = game_from_db.winners + player.name + " "  # определили победителя/победителей
        coosh = int(game_from_db.pot / len(game_from_db.winners.split()))
        for player in players_db:
            if player.win:
                print(f"{player.name} получает {coosh}")
                player.chips += coosh