def give_possible_responses(players_db, game_from_db, fa_num):
    players_db[fa_num].stake_gap = game_from_db.highest_stake - players_db[fa_num].stake
    players_db[fa_num].possible_responses = ""
    if players_db[fa_num].stake_gap > 0:
        players_db[fa_num].possible_responses += "fold "
        if players_db[fa_num].stake_gap > players_db[fa_num].chips:
            players_db[fa_num].possible_responses += "all-in "
        if players_db[fa_num].stake_gap == players_db[fa_num].chips:
            players_db[fa_num].possible_responses += "call "
        if players_db[fa_num].stake_gap < players_db[fa_num].chips:
            players_db[fa_num].possible_responses += "call "
            players_db[fa_num].possible_responses += "raise "
            players_db[fa_num].possible_responses += "all-in "
    if players_db[fa_num].stake_gap == 0:
        if players_db[fa_num].chips > 0:
            players_db[fa_num].possible_responses += "check "
            players_db[fa_num].possible_responses += "raise "
            players_db[fa_num].possible_responses += "fold "
            players_db[fa_num].possible_responses += "all-in "
        else:
            players_db[fa_num].possible_responses += "check"
            players_db[fa_num].possible_responses += "fold"
