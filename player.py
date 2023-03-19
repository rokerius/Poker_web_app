class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.chips = 0  # playerBalance
        self.stake = 0  # Ставка
        self.stake_gap = 0  # Число фишек, которые нужно положить, чтобы продолжить раунд
        self.cards = []  # Список карт у игрока в данный момент
        self.score = []
        self.fold = False  # Пас
        self.ready = False  # Игрок готов к продолжению игры
        self.all_in = False
        self.list_of_special_attributes = []  # см. dissection
        self.win = False

    def __repr__(self):  # То как он будет выглядеть
        name = self.name
        return name


player_1 = Player("Boris The Animal")