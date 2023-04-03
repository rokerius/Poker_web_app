def row_1(game_from_db, players_db, sb_num, bb_num):
    if game_from_db.sb > players_db[sb_num].chips:  # Если нет фишек даже на малый блайнд
        players_db[sb_num].stake += players_db[sb_num].chips  # Вклад
        game_from_db.pot += players_db[sb_num].chips  # Банк
        players_db[sb_num].chips = 0  # Фишки игрока
        print(f"{players_db[sb_num].name} ставит все что осталось")
        game_from_db.highest_stake = players_db[sb_num].chips
        players_db[sb_num].all_in = True
    else:
        players_db[sb_num].chips -= game_from_db.sb  # Фишки игрока
        players_db[sb_num].stake += game_from_db.sb  # Вклад
        game_from_db.pot += game_from_db.sb  # Банк
        game_from_db.highest_stake = game_from_db.sb
        print(players_db[sb_num].name + " sb: - " + str(game_from_db.sb))

    if game_from_db.sb * 2 > players_db[bb_num].chips:
        players_db[bb_num].stake += players_db[bb_num].chips  # Фишки игрока
        players_db[bb_num].chips = 0  # Вклад
        game_from_db.pot += players_db[bb_num].chips  # Банк
        print(f"{players_db[bb_num].name} ставит все что осталось")
        game_from_db.highest_stake = players_db[bb_num].chips
        players_db[bb_num].all_in = True
    else:
        players_db[bb_num].chips -= game_from_db.sb * 2  # Фишки игрока
        players_db[bb_num].stake += game_from_db.sb * 2  # Вклад
        game_from_db.pot += game_from_db.sb * 2  # Банк
        game_from_db.highest_stake = game_from_db.sb * 2
        print(players_db[sb_num].name + " bb: - " + str(game_from_db.sb * 2))

    game_from_db.id_p_now = game_from_db.players.split().index(game_from_db.fa_name)
    game_from_db.count_smth = 1
    game_from_db.row = int(game_from_db.row) + 1
    print("changed id_p_now on " + str(game_from_db.id_p_now))
    print("changed count_smth on " + str(game_from_db.count_smth))