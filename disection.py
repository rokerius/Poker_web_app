from player import Player


P1 = Player("1")
P2 = Player("2")
P3 = Player("3")
P4 = Player("4")
P5 = Player("5")
P6 = Player("6")

players = [P1, P2, P3, P4, P5, P6]


def establish_player_attributes(list_of_players_not_out):  # Статусы игроков. Аргумент: список играющих игроков
    address_assignment = 0
    dealer = list_of_players_not_out[address_assignment]  # Первый игрок - диллер
    dealer.list_of_special_attributes.append("dealer")  # Добавляем игроку этот статус
    address_assignment += 1
    address_assignment %= len(list_of_players_not_out)  # А так мы проверяем / переходим в начало списка игроков

    small_blind = list_of_players_not_out[address_assignment]  # Второй - малый блайнд
    small_blind.list_of_special_attributes.append("small blind")
    address_assignment += 1
    address_assignment %= len(list_of_players_not_out)

    big_blind = list_of_players_not_out[address_assignment]  # Третий - большой блайнд
    big_blind.list_of_special_attributes.append("big blind")
    address_assignment += 1
    address_assignment %= len(list_of_players_not_out)

    first_actor = list_of_players_not_out[address_assignment]
    first_actor.list_of_special_attributes.append("first actor")  # Четвертый - первый ходящий во втором раунде
    list_of_players_not_out.append(list_of_players_not_out.pop(0))

establish_player_attributes(players)

for player in players:
    print(f"Игрок {player.name} - {player.list_of_special_attributes}")