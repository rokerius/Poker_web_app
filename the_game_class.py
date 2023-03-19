import itertools
from collections import Counter

from asking import Replies
from cards import deck
from player import Player


class Game(object):
    def __init__(self):
        self.game_over = False
        self.acting_player = Player()
        self.possible_responses = []
        self.cards = []
        self.pot = 0
        self.pot_in_play = 0
        self.list_of_players = []
        self.dealer = Player()
        self.small_blind = Player()
        self.big_blind = Player()
        self.first_actor = Player()
        self.winners = []
        self.deck = deck
        self.start_setup = Replies()

        while True:
            self.start_setup.ask_start_info()
            self.number_of_players = len(self.start_setup.app_players)
            for name in self.start_setup.app_players:
                if name != "":
                    self.list_of_players.append(Player(name))
            self.starting_chips = int(self.start_setup.app_startchips)
            for player in self.list_of_players:
                player.chips = self.starting_chips
            self.count_smth = 0
            self.small_blind_amount = int(self.start_setup.app_sb)
            self.big_blind_amount = self.small_blind_amount * 2
            print(self.list_of_players)
            if 1 < self.number_of_players < 11 and self.starting_chips > 0 and \
                    self.starting_chips > self.small_blind_amount > 0:
                break
            else:
                self.list_of_players.clear()
                print("(!) Ошибка ввода первоначальных данных")

        self.winner = []
        self.attribute_list = ["dealer", "small blind", "big blind", "first action"]
        self.highest_stake = 0
        self.fold_list = []
        self.round_ended = False
        self.round_counter = 0
        self.fold_out = False
        self.list_of_players_not_out = self.list_of_players
        self.number_of_player_not_out = len(self.list_of_players)

    def print_round_info(self):
        print("\n" * 10)
        print("------------------------------------------------------------------")
        for player in self.list_of_players:
            print(f"Имя: {player.name}", end="; ")
            print(f"Карты: {player.cards}")
            print(f"Фишки: {player.chips}", end="; ")
            print(f"Special Attributes: {player.list_of_special_attributes}")
            if player.fold:
                print(f"Пасанул")
            if player.all_in:
                print(f"All-in")
            print(f"Ставка: {player.stake}", end=", ")
            print(f"нужно докинуть: {player.stake_gap}")
            print("\n")
        print(f"Банк: {self.pot}", end=" ")
        print(f"Карты на столе: {self.cards}")
        print("------------------------------------------------------------------")

    def give_player_attributes(self):  # Статусы игроков
        assi_numero = self.round_counter % len(self.list_of_players_not_out)

        self.dealer = self.list_of_players_not_out[assi_numero]
        self.dealer.list_of_special_attributes.append("dealer")
        assi_numero += 1
        assi_numero %= len(self.list_of_players_not_out)

        self.small_blind = self.list_of_players_not_out[assi_numero]
        self.small_blind.list_of_special_attributes.append("small blind")
        assi_numero += 1
        assi_numero %= len(self.list_of_players_not_out)

        self.big_blind = self.list_of_players_not_out[assi_numero]
        self.big_blind.list_of_special_attributes.append("big blind")
        assi_numero += 1
        assi_numero %= len(self.list_of_players_not_out)

        self.first_actor = self.list_of_players_not_out[assi_numero]
        self.first_actor.list_of_special_attributes.append("first actor")

        self.round_counter += 1

    def deal_razdacha(self):  # Раздача
        for player in self.list_of_players_not_out:
            self.deck.deal(player, 2)

    def deal_flop(self):  # Флоп
        self.deck.deal(self, 3)

    def deal_turn(self):  # Тёрн
        self.deck.deal(self, 1)

    def deal_river(self):  # Ривер
        self.deck.deal(self, 1)

    def hand_scorer(self, player):  # подсчет комбинаций
        seven_cards = player.cards + self.cards
        all_hand_combos = list(itertools.combinations(seven_cards, 5))
        # пример: combinations('ABCD', 2)  AB AC AD BC BD CD
        list_of_all_score_possibilities = []
        for i in all_hand_combos:
            suit_list = []
            value_list = []
            for j in i:
                suit_list.append(j.suit)
                value_list.append(j.value)

            value_list.sort()
            value_list.reverse()
            score = [0, 0, 0, value_list[0], value_list[1], value_list[2], value_list[3], value_list[4]]
            # Ранг
            # Ценность
            # Если две пары - ценность наименьшей
            # Кикеры (но считаем все 5 карт)
            list_of_pair_values = []
            other_cards = []
            pair_win = False
            pair_value = 0
            value_counter = dict(Counter(value_list))  # Используем библиотеку Collections,
            # используем Counter (Подсчет количества повторений элементов в последовательности)
            # >> > cnt = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])
            # >> > dict(cnt)
            # {'blue': 3, 'red': 2, 'green': 1}
            for value_name, count in value_counter.items():  # Ищем пары
                if count == 2:
                    pair_win = True
                    pair_value = value_name
                    list_of_pair_values.append(value_name)
            if pair_win:
                for value in value_list:
                    if value not in list_of_pair_values:
                        other_cards.append(value)
                other_cards.sort()
                other_cards.reverse()
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
            if sorted(value_list) == [0, 1, 2, 3, 12] and len(set(suit_list)) == 1:  # Стрит-флеш с тузом
                score[0] = 8
                score[1] = 3
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)) and len(set(suit_list)) == 1:
                # Стрит-флеш
                score[0] = 8
                score[1] = max(value_list)
                if max(value_list) == 12:  # Флеш-рояль
                    score[0] = 9
            list_of_all_score_possibilities.append(score)
        player.score = max(list_of_all_score_possibilities)  # Подсчет комбинаций

    def score_all(self):  # Подсчитываем очки у всех
        for player in self.list_of_players_not_out:
            self.hand_scorer(player)

    def find_winners(self):  # Ищем победителя
        print("\n --------winners--------")
        if self.fold_out:
            for player in list(set(self.winners)):
                coosh = int((self.pot / len(list(set(self.winners)))))
                player.chips += coosh
                print(f"{player.name} выиграл {coosh} фишек!")
        else:
            list_of_stakes = []
            for player in self.list_of_players_not_out:
                if not player.fold:
                    list_of_stakes.append(player.score)
            max_score = max(list_of_stakes)  # это мы нашли максимальное колличество очков
            for player in self.list_of_players_not_out:
                if player.score == max_score and not player.fold:
                    player.win = True
                    self.winners.append(player)  # определили победителя/победителей
            coosh = int(self.pot/len(self.winners))
            for player in self.winners:
                print(f"{player.name} получает {coosh}")
                player.chips += coosh
                self.pot -= coosh  # Дали победителям денег

            for player in self.list_of_players_not_out:
                if player.win:
                    print("\n" + player.name + ": " + str(player.cards) + "     <-- WINNER \n   ")
                elif player.fold:
                    print("\n" + player.name + ": " + str(player.cards) + "\n   " + "[FOLDED]")
                else:
                    print("\n" + player.name + ": " + str(player.cards) + "\n   ")
                print(f"    Score: {player.score} \n    Фишек: {player.chips}")

    def clear_board(self):  # Очистка
        print("\n --------clearing board--------")
        self.possible_responses.clear()
        self.cards.clear()
        self.deck = deck
        self.deck.shuffle()
        self.pot = 0
        self.winners.clear()
        self.highest_stake = 0
        self.fold_list.clear()
        self.fold_out = False
        self.round_ended = False
        for player in self.list_of_players:
            player.score.clear()
            player.cards.clear()
            player.stake = 0
            player.stake_gap = 0
            player.ready = False
            player.all_in = False
            player.fold = False
            player.list_of_special_attributes.clear()
            player.win = False

    def end_round(self):
        print(print("\n --------GLOBAL winners--------"))
        for player in self.list_of_players_not_out:
            if player.chips <= 0:
                self.list_of_players_not_out.remove(player)
                print(f"{player.name} выходит из игры")
        if len(set(self.list_of_players_not_out)) == 1:
            self.game_over = True
            print(f"Остался только: {self.list_of_players_not_out[0]} и него фишек:",
                  self.list_of_players_not_out[0].chips)
            exit(0)

        end_setup = Replies()
        end_setup.end_ask()
        new_round = end_setup.end_ask()

        if new_round:
            print("\n\n---------------------НАЧИНАЕТСЯ НОВЫЙ РАУНД---------------------\n")
            self.clear_board()
        else:
            print("конец")
            exit(0)
            # Конец раунда

    def answer(self, player):  # Получаем ответ у игрока
        print("\n")
        player.stake_gap = self.highest_stake - player.stake  # Сколько нужно вложить игроку, чтобы остаться
        if player.all_in or player.fold or self.fold_out:  # Если игрок не ходит
            return True
        if player.chips <= 0:  # ALL-IN
            print(f"{player.name} идет В ALL-IN")
            player.all_in = True
        print(f"Наивысщая ставка: {self.highest_stake}")
        print(f"Докиньте {player.stake_gap} чтобы остаться")
        print(f"У вас: {player.chips}")
        self.possible_responses.clear()  # Возможные выборы
        if player.stake_gap > 0:
            self.possible_responses.append("fold")
            if player.stake_gap >= player.chips:
                self.possible_responses.append("all_in")
            if player.stake_gap < player.chips:
                self.possible_responses.append("call")
                self.possible_responses.append("raise")
                self.possible_responses.append("all_in")
        if player.stake_gap == 0:
            self.possible_responses.append("check")
            self.possible_responses.append("raise")
            self.possible_responses.append("fold")
            self.possible_responses.append("all_in")
        while True:
            print(self.possible_responses)
            print("Ходит: ", player)

            ask_action = Replies()
            response = ask_action.ask_responce()

            if response not in self.possible_responses:
                print("error: ты что-то не то выбрал")
                continue

            if response == "fold":
                player.fold = True
                self.fold_list.append(player)
                if len(self.fold_list) == (len(self.list_of_players_not_out) - 1):  # Все пас кроме одного
                    for player in self.list_of_players_not_out:
                        if player not in self.fold_list:
                            self.fold_out = True
                            self.winners.append(player)
                            print(f"{player} выиграл, все - пас")
                            for player in self.winners:
                                player.win = True
                            self.round_ended = True
                return True
            if response == "call":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                return True
            if response == "check":
                return True
            if response == "raise":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                while True:
                    print(f"Сколько {player.name} ставит? (доступно: {player.chips})\n->")

                    ask_ri = Replies()
                    bet = ask_ri.ask_ri()

                    if bet > player.chips or bet <= 0:
                        print("error: неверный ввод")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} ставит все!")
                        player.all_in = True
                    player.stake += bet  # Вклад
                    self.pot += bet  # Банк
                    player.chips -= bet  # Фищки игрока
                    self.highest_stake = player.stake
                    self.count_smth = 0
                    return True
            if response == "all_in":
                player.stake += player.chips  # Вклад
                self.pot += player.chips  # Банк
                player.stake_gap -= player.chips  # Фишки игрока
                self.highest_stake = player.stake
                player.stake_gap = 0
                player.chips = 0
                print(f"{player.name} ставит все!")
                player.all_in = True
                self.count_smth = 0
                return True

    def ask_players(self):  # проходим круг
        self.count_smth = 0
        starting_index = self.list_of_players_not_out.index(self.first_actor)
        for player in self.list_of_players_not_out:
            player.ready = False
        while True:
            self.acting_player = self.list_of_players_not_out[starting_index]
            player_ready = self.answer(self.list_of_players_not_out[starting_index])  # Спрашиваем у игрока
            starting_index += 1
            starting_index %= len(self.list_of_players_not_out)  # Та самая гениальная проверка
            if player_ready:  # То есть ответил, он нам True возвращает всегда
                self.count_smth += 1
            if self.count_smth == len(self.list_of_players_not_out):  # Круг закончился!
                break

    def act_one(self):  # Начало (малый и большой блайнды)
        if self.small_blind_amount > self.small_blind.chips:  # Если нет фишек даже на малый блайнд
            self.small_blind.stake += self.small_blind.chips  # Вклад
            self.pot += self.small_blind.chips  # Банк
            self.small_blind.chips = 0  # Фишки игрока
            print(f"{self.small_blind.name} ставит все что осталось(")
            self.highest_stake = self.small_blind.chips
            self.small_blind.all_in = True
        else:
            self.small_blind.chips -= self.small_blind_amount  # Фишки игрока
            self.small_blind.stake += self.small_blind_amount  # Вклад
            self.pot += self.small_blind_amount  # Банк
            self.highest_stake = self.small_blind_amount

        if self.big_blind_amount > self.big_blind.chips:
            self.big_blind.stake += self.big_blind.chips  # Фишки игрока
            self.big_blind.chips = 0  # Вклад
            self.pot += self.big_blind.chips  # Банк
            print(f"{self.big_blind} ставит все что осталось(")
            self.highest_stake = self.big_blind.chips
            self.big_blind.all_in = True
        else:
            self.big_blind.chips -= self.big_blind_amount  # Фишки игрока
            self.big_blind.stake += self.big_blind_amount  # Вклад
            self.pot += self.big_blind_amount  # Банк
            self.highest_stake = self.big_blind_amount
        self.ask_players()

    # def score_interpreter(player):
    #     list_of_hand_types = ["Старшая карта", "Пара", "Две пары", "Сет", "Стрит", "Флеш",
    #                           "Фул Хауз","Каре", "Стрит-Флеш", "Флеш Рояль"]
    #     list_of_values_to_interpret = ["Двойка", "Тройка", "Четверка", "Пятерка", "Шестерка",
    #                                   "Семь", "Восемь", "Девять", "Десять",
    #                                    "Валет", "Дама", "Король", "Туз"]
    #     hand_type = list_of_hand_types[player.score[0]]
    #     mod1 = list_of_values_to_interpret[player.score[1]]
    #     mod2 = list_of_values_to_interpret[player.score[2]]
    #     mod3 = list_of_values_to_interpret[player.score[3]]
    #     if player.score[0] == 0:
    #         return hand_type + ": " + mod3
    #     if player.score[0] == 1:
    #         return hand_type + ": " + mod1
    #     if player.score[0] == 2:
    #         return hand_type + ": " + mod1 + " и " + mod2
    #     if player.score[0] == 3:
    #         return hand_type + ": " + mod1
    #     if player.score[0] == 4:
    #         return hand_type + ": до " + mod1
    #     if player.score[0] == 5:
    #         return hand_type + ": до " + mod1
    #     if player.score[0] == 6:
    #         return hand_type + ": " + mod1 + " и " + mod2
    #     if player.score[0] == 7:
    #         return hand_type + ": " + mod1
    #     if player.score[0] == 8:
    #         return hand_type + ": до " + mod1
    #     if player.score[0] == 9:
    #         return hand_type
