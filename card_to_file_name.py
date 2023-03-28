def to_file_name(value, suit):
    value_name = ""
    suit_name = ""
    if value == 0:
        value_name = "Two"
    if value == 1:
        value_name = "Three"
    if value == 2:
        value_name = "Four"
    if value == 3:
        value_name = "Five"
    if value == 4:
        value_name = "Six"
    if value == 5:
        value_name = "Seven"
    if value == 6:
        value_name = "Eight"
    if value == 7:
        value_name = "Nine"
    if value == 8:
        value_name = "Ten"
    if value == 9:
        value_name = "Jack"
    if value == 10:
        value_name = "Queen"
    if value == 11:
        value_name = "King"
    if value == 12:
        value_name = "Ace"
    if suit == 0:
        suit_name = "Diamonds"  # "Бубы"
    if suit == 1:
        suit_name = "Clubs"  # "Трефы"
    if suit == 2:
        suit_name = "Hearts"  # "Черви"
    if suit == 3:
        suit_name = "Spades"  # "Пики"
    return value_name + " of " + suit_name

