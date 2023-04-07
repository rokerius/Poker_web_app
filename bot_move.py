def bot_move(game_from_db, bot):
    bot.stake_gap = game_from_db.highest_stake - bot.stake

    if bot.stake_gap == 0:
        return "check"
    else:
        if bot.chips >= bot.stake_gap:
            return "call"
        else:
            return "fold"
