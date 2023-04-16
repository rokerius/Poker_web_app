from poker_app import act


class Replies(object):
    def __init__(self):
        self.answer = None
        self.app_players = 0
        self.app_sb = 0
        self.app_startchips = 0

    def ask_start_info(self):
        self.app_players = act.app_players
        self.app_startchips = act.app_start_chips
        self.app_sb = act.app_sb

    def end_ask(self):
        ans = input("Заново?")
        if ans.lower() == "да" or ans.lower() == "yes":
            return True
        return False

    def ask_responce(self):
        ans = input("Ваше действие? \n")
        return ans

    def ask_ri(self):
        return int(input("Сколько ставим?"))





