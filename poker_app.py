from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from disection import disection
from find_winner import find_winner
from hand_scorer import hand_scorer
from one_row import one_row
from cards import deck
from card_to_file_name import to_file_name
from possible_responses import give_possible_responses
from row_1 import row_1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class WEB_Replies(object):
    def __init__(self):
        self.answer = None
        self.app_players = []
        self.app_sb = 0
        self.app_chips = 0
        self.possible_responses = ["fold", "check", "call", "all-in", "raise"]

    def start_info_update_players(self, players):
        for i in range(len(players.split())):
            self.app_players.append(players.split()[i])

    def start_info_update_chips(self, start_chips, small_blind):
        self.app_chips = start_chips
        self.app_sb = small_blind


class Player_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    chips = db.Column(db.Integer, nullable=False)
    stake = db.Column(db.Integer, default=0, nullable=False)
    stake_gap = db.Column(db.Integer, default=0, nullable=False)
    k_wins = db.Column(db.Integer, default=0, nullable=False)
    cards = db.Column(db.String(64), nullable=False)
    int_cards = db.Column(db.String(32), nullable=False)
    fold = db.Column(db.Boolean, default=False, nullable=False)
    all_in = db.Column(db.Boolean, default=False, nullable=False)
    win = db.Column(db.Boolean, default=False, nullable=False)
    ready = db.Column(db.Boolean, default=False, nullable=False)
    list_of_special_attributes = db.Column(db.String(128), nullable=False)
    possible_responses = db.Column(db.String(128), nullable=False)
    score = db.Column(db.String(128), default="", nullable=False)

    # game_id = db.Column(db.Integer, db.ForeignKey('game_db.id'), nullable=False)
    # game = db.relationship('Game_db', backref=db.backref('players', lazy=True))


class Game_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_chips = db.Column(db.Integer, nullable=False)
    sb = db.Column(db.Integer, nullable=False)
    players = db.Column(db.String(512), nullable=False)
    number_of_players = db.Column(db.Integer, nullable=False)
    cards_on_table = db.Column(db.String(128), nullable=False)
    int_cards_on_table = db.Column(db.String(32), nullable=False)
    dealer = db.Column(db.String(32), nullable=False)
    sb_name = db.Column(db.String(32), nullable=False)
    bb_name = db.Column(db.String(32), nullable=False)
    fa_name = db.Column(db.String(32), nullable=False)
    highest_stake = db.Column(db.Integer, nullable=False, default=0)
    pot = db.Column(db.Integer, nullable=False, default=0)
    row = db.Column(db.Integer, nullable=False, default=0)
    id_p_now = db.Column(db.Integer, nullable=False, default=0)
    count_smth = db.Column(db.Integer, nullable=False, default=0)
    cards_show_status = db.Column(db.Integer, nullable=False, default=0)
    n_round = db.Column(db.Integer, nullable=False, default=0)
    fold_list = db.Column(db.String(512), default=" ", nullable=False)
    winners = db.Column(db.String(512), default=" ", nullable=False)
    fold_out = db.Column(db.Boolean, default=False, nullable=False)
    round_ended = db.Column(db.Boolean, default=False, nullable=False)
    bet_ask = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Game%r>' % self.id, self.start_chips, self.sb, self.players


act = WEB_Replies()


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def start_asking():
    if request.method == "POST":
        start_chips = int(request.form['start_chips'])
        small_blind = int(request.form['small_blind'])
        act.start_info_update_chips(start_chips, small_blind)
        return redirect('/players')
    else:
        return render_template("start-page.html")


@app.route('/players', methods=['POST', 'GET'])
def players():
    if request.method == "POST":
        player1 = request.form['player1']
        player2 = request.form['player2']
        player3 = request.form['player3']
        player4 = request.form['player4']
        player5 = request.form['player5']
        player6 = request.form['player6']

        players_str = player1 + " " + player2 + " " + player3 + " " + \
                      player4 + " " + player5 + " " + player6
        act.start_info_update_players(players_str)

        # disection
        address_assignment = 0
        dealer = str(act.app_players[address_assignment])
        address_assignment += 1
        address_assignment %= len(players_str.split())
        sb_name = str(act.app_players[address_assignment])
        address_assignment += 1
        address_assignment %= len(players_str.split())
        bb_name = str(act.app_players[address_assignment])
        address_assignment += 1
        address_assignment %= len(players_str.split())
        fa_name = str(act.app_players[address_assignment])

        Game_db.query.filter(Game_db.id != -1).delete()
        Player_db.query.filter(Player_db.id != -1).delete()

        cards_on_table = ""
        int_cards_on_table = ""
        for i in range(5):
            card = deck.pop(0)
            strcard = to_file_name(card.value, card.suit)
            cards_on_table += strcard + ","
            int_cards_on_table += str(card.value) + " " + str(card.suit) + " "

        game = Game_db(start_chips=act.app_chips, sb=act.app_sb,
                       players=players_str, number_of_players=len(players_str.split()),
                       cards_on_table=cards_on_table, int_cards_on_table=int_cards_on_table,
                       dealer=dealer, sb_name=sb_name, bb_name=bb_name,
                       fa_name=fa_name, pot=0)
        db.session.add(game)
        db.session.commit()

        for player_name in players_str.split():
            card1 = deck.pop(0)
            strcard1 = to_file_name(card1.value, card1.suit)
            card2 = deck.pop(0)
            strcard2 = to_file_name(card2.value, card2.suit)
            cards_of_players = strcard1 + "," + strcard2
            int_cards_of_players = str(card1.value) + " " + str(card1.suit) + " " + \
                                   str(card2.value) + " " + str(card2.suit) + " "

            l_of_sa = ""
            if player_name == game.dealer:
                l_of_sa = l_of_sa + "dealer "
            if player_name == game.sb_name:
                l_of_sa = l_of_sa + "sb "
            if player_name == game.bb_name:
                l_of_sa = l_of_sa + "bb "
            if player_name == game.fa_name:
                l_of_sa = l_of_sa + "fa "
            player = Player_db(name=player_name, chips=act.app_chips, cards=cards_of_players,
                               int_cards=int_cards_of_players,
                               list_of_special_attributes=l_of_sa,
                               possible_responses=" ".join(act.possible_responses))
            db.session.add(player)
            db.session.commit()

        print("edited")
        return redirect('/the_game')
    else:
        return render_template("players_page.html")


@app.route('/the_game', methods=['POST', 'GET'])
def the_game():
    if request.method == "GET":
        game_from_db = Game_db.query.first()
        players_db = Player_db.query.order_by(Player_db.id).all()
        return render_template("the_game.html", game=game_from_db, players_db=players_db,
                               id_p_now=act.app_players.index(game_from_db.fa_name))
    else:
        game_from_db = Game_db.query.first()
        players_db = Player_db.query.order_by(Player_db.id).all()
        sb_num = act.app_players.index(game_from_db.sb_name)
        bb_num = act.app_players.index(game_from_db.bb_name)
        fa_num = act.app_players.index(game_from_db.fa_name)

        # Если игрок хочет что-то поставить
        if game_from_db.bet_ask:
            print("bet_ask")
            bet = int(request.form['bet'])
            if bet > players_db[game_from_db.id_p_now].chips or bet <= 0 \
                    or bet < players_db[game_from_db.id_p_now].stake_gap:
                print("error: неверный ввод")
            else:
                if bet == players_db[game_from_db.id_p_now].chips:
                    print(f"{players_db[game_from_db.id_p_now].name} ставит всё!")
                    players_db[game_from_db.id_p_now].all_in = True
                players_db[game_from_db.id_p_now].stake_gap = 0
                players_db[game_from_db.id_p_now].stake += bet  # Вклад
                game_from_db.pot += bet  # Банк
                players_db[game_from_db.id_p_now].chips -= bet  # Фищки игрока
                game_from_db.highest_stake = players_db[game_from_db.id_p_now].stake
                game_from_db.count_smth = 1
                game_from_db.id_p_now += 1
                game_from_db.id_p_now %= len(game_from_db.players.split())
                game_from_db.bet_ask = False
                give_possible_responses(players_db, game_from_db, game_from_db.id_p_now)

        else:
            # Круг
            if int(game_from_db.row) == 2:
                response = request.form['player_action']
                print(players_db[game_from_db.id_p_now].name, "играет")
                one_row(game_from_db, players_db, response)
                give_possible_responses(players_db, game_from_db, game_from_db.id_p_now)

            # Начать
            if int(game_from_db.row) == 0:
                print("The Game started")
                game_from_db.row = request.form['row']
                row_1(game_from_db, players_db, fa_num, sb_num, bb_num)
                give_possible_responses(players_db, game_from_db, fa_num)

            # Междукружье
            if int(game_from_db.row) == 3:
                game_from_db.cards_show_status += 1
                if game_from_db.cards_show_status == 4:
                    print("Counting")
                    game_from_db.row = 4
                else:
                    game_from_db.row -= 1
                    game_from_db.count_smth = 1
                    game_from_db.id_p_now = sb_num
                give_possible_responses(players_db, game_from_db, sb_num)

            # Выбор продолжать или нет
            if int(game_from_db.row) == 5:
                game_from_db.row = request.form['row']
                print("выбор")

            # Следующая игра
            if int(game_from_db.row) == 6:
                print("Следующая игра")
                for player in players_db:
                    if player.chips <= 0:
                        db.session.delete(player)
                        game_from_db.number_of_players -= 1
                        pl = game_from_db.players.split()
                        pl.remove(player.name)
                        game_from_db.players = " ".join(pl)
                        print(f"{player.name} выходит из игры")
                if game_from_db.number_of_players == 1:
                    game_from_db.row = 7
                    print(f"Остался только: {game_from_db.players.split()[0]}")
                else:
                    game_from_db.pot = 0
                    game_from_db.row = 0
                    game_from_db.n_round += 1
                    game_from_db.round_ended = False
                    game_from_db.cards_show_status = 0
                    game_from_db.winners = ""
                    game_from_db.fold_out = False
                    game_from_db.highest_stake = 0

                    disection(game_from_db, game_from_db.n_round)

                    game_from_db.cards_on_table = ""
                    game_from_db.int_cards_on_table = ""

                    for i in range(5):
                        card = deck.pop(0)
                        strcard = to_file_name(card.value, card.suit)
                        game_from_db.cards_on_table += strcard + ","
                        game_from_db.int_cards_on_table += str(card.value) + " " + str(card.suit) + " "

                    for player_name in players_db:
                        card1 = deck.pop(0)
                        strcard1 = to_file_name(card1.value, card1.suit)
                        card2 = deck.pop(0)
                        strcard2 = to_file_name(card2.value, card2.suit)
                        player_name.cards_of_players = strcard1 + "," + strcard2
                        player_name.int_cards_of_players = str(card1.value) + " " + str(card1.suit) + " " + \
                                               str(card2.value) + " " + str(card2.suit) + " "
                        player_name.score = ""
                        player_name.stake = 0
                        player_name.all_in = False
                        player_name.fold = False
                        player_name.win = False
                        l_of_sa = ""
                        if player_name == game_from_db.dealer:
                            l_of_sa = l_of_sa + "dealer "
                        if player_name == game_from_db.sb_name:
                            l_of_sa = l_of_sa + "sb "
                        if player_name == game_from_db.bb_name:
                            l_of_sa = l_of_sa + "bb "
                        if player_name == game_from_db.fa_name:
                            l_of_sa = l_of_sa + "fa "
                        player_name.l_of_sa = l_of_sa

            # Конец
            if int(game_from_db.row) == 7:
                print("Конец")
                return redirect('/statistics')

            # Подсчет комбинаций
            if int(game_from_db.row) == 4:
                hand_scorer(game_from_db, players_db)
                find_winner(game_from_db, players_db)
                game_from_db.round_ended = True
                game_from_db.row = int(game_from_db.row) + 1
                print("row changed on " + str(game_from_db.row))

        db.session.commit()

        return render_template("the_game.html", game=game_from_db, players_db=players_db,
                               id_p_now=game_from_db.id_p_now)


@app.route('/statistics')
def statistics():
    game_from_db = Game_db.query.first()
    players_db = Player_db.query.order_by(Player_db.id).all()
    return render_template("statistics.html", game=game_from_db, players_db=players_db)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
