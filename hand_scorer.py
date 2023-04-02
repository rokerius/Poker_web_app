import itertools
from collections import Counter


def hand_scorer(game_from_db, players_db):
    for p_num in range(game_from_db.number_of_players):
        seven_cards_str = game_from_db.int_cards_on_table + " " + players_db[p_num].int_cards
        seven_cards = []
        for i in range(7):
            seven_cards.append([seven_cards_str.split()[i * 2], seven_cards_str.split()[i * 2 + 1]])
        all_hand_combos = list(itertools.combinations(seven_cards, 5))
        list_of_all_score_possibilities = []
        for i in all_hand_combos:
            suit_list = []
            value_list = []
            for j in i:
                suit_list.append(int(j[1]))
                value_list.append(int(j[0]))
            value_list.sort(reverse=True)
            score = [0, 0, 0, value_list[0], value_list[1], value_list[2], value_list[3], value_list[4]]
            list_of_pair_values = []
            other_cards = []
            pair_win = False
            pair_value = 0
            value_counter = dict(Counter(value_list))
            for value_name, count in value_counter.items():  # Ищем пары
                if count == 2:
                    pair_win = True
                    pair_value = value_name
                    list_of_pair_values.append(value_name)
            if pair_win:
                for value in value_list:
                    if value not in list_of_pair_values:
                        other_cards.append(value)
                other_cards.sort(reverse=True)
                if len(list_of_pair_values) == 1:  # Пара
                    score[0] = 1
                    score[1] = list_of_pair_values[0]
                    try:
                        score[2] = other_cards[0]
                        score[3] = other_cards[1]
                        score[4] = other_cards[2]
                        score[5] = other_cards[3]
                        score[6] = other_cards[4]
                    except IndexError:
                        pass
                if len(list_of_pair_values) == 2:  # Две пары
                    score[0] = 2
                    score[1] = max(list_of_pair_values)
                    score[2] = min(list_of_pair_values)
                    try:
                        score[3] = other_cards[0]
                        score[4] = other_cards[1]
                        score[5] = other_cards[2]
                        score[6] = other_cards[3]
                        score[7] = other_cards[4]
                    except IndexError:
                        pass
            three_of_a_kind_value = 0
            other_cards = []
            three_of_a_kind_win = False
            for value_name, count in value_counter.items():  # Ищем тройки
                if count == 3:
                    three_of_a_kind_win = True
                    three_of_a_kind_value = value_name
            if three_of_a_kind_win:  # Сет
                for value in value_list:
                    if value != three_of_a_kind_value:
                        other_cards.append(value)
                other_cards.sort()
                other_cards.reverse()
                score[0] = 3
                score[1] = three_of_a_kind_value
                try:
                    score[2] = other_cards[0]
                    score[3] = other_cards[1]
                    score[4] = other_cards[2]
                    score[5] = other_cards[3]
                    score[6] = other_cards[4]
                except IndexError:
                    pass
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)):  # Стрит
                score[0] = 4
                score[1] = max(value_list)
            if sorted(value_list) == [0, 1, 2, 3, 12]:  # Стрит с тузом и двойкой
                score[0] = 4
                score[1] = 3
            if len(set(suit_list)) == 1:  # Флеш
                score[0] = 5
                score[1] = max(value_list)
            if three_of_a_kind_win and pair_win:  # Фулл-хауз
                score[0] = 6
                score[1] = three_of_a_kind_value
                score[2] = pair_value
            four_of_a_kind_value = None
            other_card_value = None
            four_of_a_kind = False
            for value_name, count in value_counter.items():  # Ищем Каре
                if count == 4:
                    four_of_a_kind_value = value_name
                    four_of_a_kind = True
            for value in value_list:
                if value != four_of_a_kind_value:
                    other_card_value = value
            if four_of_a_kind:  # Каре
                score[0] = 7
                score[1] = four_of_a_kind_value
                score[2] = other_card_value
            if sorted(value_list) == [0, 1, 2, 3, 12] and len(
                    set(suit_list)) == 1:  # Стрит-флеш с тузом
                score[0] = 8
                score[1] = 3
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)) and len(
                    set(suit_list)) == 1:
                # Стрит-флеш
                score[0] = 8
                score[1] = max(value_list)
                if max(value_list) == 12:  # Флеш-рояль
                    score[0] = 9
            list_of_all_score_possibilities.append(score)
        maxscore = max(list_of_all_score_possibilities)
        lol = ""
        for elem in maxscore:
            lol = lol + " " + str(elem)
        players_db[p_num].score = lol