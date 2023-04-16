def bot_move_1(game, bot):
    print('Привет, я Бот №1')
    bot.stake_gap = game['highest_stake'] - bot.stake

    if bot.stake_gap == 0:
        return "check"
    else:
        if bot.chips >= bot.stake_gap:
            return "call"
        else:
            return "fold"


def bot_move_2(game, bot):
    print('Привет, я Бот №2')
    bot.stake_gap = game['highest_stake'] - bot.stake

    if bot.stake_gap == 0:
        bet = "raise 100"
        return bet
    else:
        if bot.chips >= bot.stake_gap:
            return "call"
        else:
            return "fold"
