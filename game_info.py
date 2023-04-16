def give_game_info(game_from_db):
    game = {
        'sb': game_from_db.sb, 'start_chips': game_from_db.start_chips,
        'players': game_from_db.players, 'all_in': game_from_db.all_in,
        'sb_name': game_from_db.sb_name, 'bb_name': game_from_db.bb_name,
        'fa_name': game_from_db.fa_name, 'fold_list': game_from_db.fold_list,
        'highest_stake': game_from_db.highest_stake,
        'cards_on_table': "", 'int_cards_on_table': ""
    }
    if game_from_db.cards_show_status == 1:
        game['cards_on_table'] = game_from_db.cards_on_table.split(',')[0] + "," + \
                                 game_from_db.cards_on_table.split(',')[1] + "," + \
                                 game_from_db.cards_on_table.split(',')[2] + ","
        game['int_cards_on_table'] = " ".join(game_from_db.int_cards_on_table.split()[0:6])
    if game_from_db.cards_show_status == 2:
        game['cards_on_table'] = game['cards_on_table'] + \
                                 game_from_db.cards_on_table.split(',')[3] + ","
        game['int_cards_on_table'] = " ".join(game_from_db.int_cards_on_table.split()[0:8])
    if game_from_db.cards_show_status == 3:
        game['cards_on_table'] = game_from_db.cards_on_table
        game['int_cards_on_table'] = game_from_db.int_cards_on_table

    return game
