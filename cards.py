import random


class Card(object):
    #  Типо конструктор
    def __init__(self, value, suit):
        self.value = value  # значение
        self.suit = suit  # масть

    #  Выводит что в классе
    def __repr__(self):
        value_name = ""
        suit_name = ""
        if self.value == 0:
            value_name = "Two"
        if self.value == 1:
            value_name = "Three"
        if self.value == 2:
            value_name = "Four"
        if self.value == 3:
             value_name = "Five"
        if self.value == 4:
            value_name = "Six"
        if self.value == 5:
            value_name = "Seven"
        if self.value == 6:
            value_name = "Eight"
        if self.value == 7:
            value_name = "Nine"
        if self.value == 8:
            value_name = "Ten"
        if self.value == 9:
            value_name = "Jack"
        if self.value == 10:
            value_name = "Queen"
        if self.value == 11:
            value_name = "King"
        if self.value == 12:
            value_name = "Ace"
        if self.suit == 0:
            suit_name = "Diamonds"  # "Бубы"
        if self.suit == 1:
            suit_name = "Clubs"  # "Трефы"
        if self.suit == 2:
            suit_name = "Hearts"  # "Черви"
        if self.suit == 3:
            suit_name = "Spades"  # "Пики"
        return value_name + " of " + suit_name


class StandardDeck(list):
    def __init__(self):
        suits = list(range(4))
        values = list(range(13))
        for i in values:
            for j in suits:
                self.append(Card(i, j))  # ЗАполняем колоду картами
        random.shuffle(self)

    def __repr__(self):
        return f"Колода карт: \n{len(self)} осталось"

    def shuffle(self):
        random.shuffle(self)

    def deal(self, location, times=1):  # location - это игрок
        for i in range(times):
            location.cards.append(self.pop(0))  # Удаляет карту из калоды и переносит ее игроку


deck = StandardDeck()
deck.shuffle()