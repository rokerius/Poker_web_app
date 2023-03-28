from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from player import Player
from cards import deck
from card_to_file_name import to_file_name

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
        self.bank = 0
        self.id_p_now = 0
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
    cards = db.Column(db.String(64), nullable=False)
    int_cards = db.Column(db.String(32), nullable=False)
    fold = db.Column(db.Boolean, default=False, nullable=False)
    all_in = db.Column(db.Boolean, default=False, nullable=False)
    list_of_special_attributes = db.Column(db.String(128), nullable=False)
    possible_responses = db.Column(db.String(128), nullable=False)

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
        game_from_db.row = request.form['row']

        dealer_num = act.app_players.index(game_from_db.dealer)
        sb_num = act.app_players.index(game_from_db.sb_name)
        bb_num = act.app_players.index(game_from_db.bb_name)
        fa_num = act.app_players.index(game_from_db.fa_name)

        if game_from_db.row == 1:
            if game_from_db.sb > players_db[sb_num].chips:  # Если нет фишек даже на малый блайнд
                players_db[sb_num].stake += players_db[sb_num].chips  # Вклад
                game_from_db.pot += players_db[sb_num].chips  # Банк
                players_db[sb_num].chips = 0  # Фишки игрока
                print(f"{players_db[sb_num].name} ставит все что осталось")
                game_from_db.highest_stake = players_db[sb_num].chips
                players_db[sb_num].all_in = True
            else:
                players_db[sb_num].chips -= game_from_db.sb  # Фишки игрока
                players_db[sb_num].stake += game_from_db.sb  # Вклад
                game_from_db.pot += game_from_db.sb  # Банк
                game_from_db.highest_stake = game_from_db.sb

            if game_from_db.sb * 2 > players_db[bb_num].chips:
                players_db[bb_num].stake += players_db[bb_num].chips  # Фишки игрока
                players_db[bb_num].chips = 0  # Вклад
                game_from_db.pot += players_db[bb_num].chips  # Банк
                print(f"{players_db[bb_num].name} ставит все что осталось")
                game_from_db.highest_stake = players_db[bb_num].chips
                players_db[bb_num].all_in = True
            else:
                players_db[bb_num].chips -= game_from_db.sb * 2  # Фишки игрока
                players_db[bb_num].stake += game_from_db.sb * 2  # Вклад
                game_from_db.pot += game_from_db.sb * 2  # Банк
                game_from_db.highest_stake = game_from_db.sb * 2

        db.session.commit()

        return render_template("the_game.html", game=game_from_db, players_db=players_db,
                               id_p_now=fa_num)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
