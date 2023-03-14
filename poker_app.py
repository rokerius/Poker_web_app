from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class WEB_Replies(object):
    def __init__(self):
        self.answer = None
        self.app_players = 0
        self.app_sb = 0
        self.app_start_chips = 0

    def start_info_update_players(self, players):
        self.app_players = players.split()

    def start_info_update_chips(self, start_chips, small_blind):
        self.app_start_chips = start_chips
        self.app_sb = small_blind


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Устанавливается по умолчанию
    name = db.Column(db.String(100), nullable=False)
    chips = db.Column(db.Integer, nullable=False)
    smth1 = db.Column(db.Integer, nullable=False)
    smth2 = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def start_asking():
    if request.method == "POST":
        start_chips = int(request.form['start_chips'])
        small_blind = int(request.form['small_blind'])
        print(start_chips, small_blind)
        act.start_info_update_chips(start_chips, small_blind)

        # article = Article(chips=start_chips, smth1=small_blind, smth2="Стартовые фишки и малый блайнд")
        #
        # try:
        #     db.session.add(article)
        #     db.session.commit()
        #     print("edited")
        #     return redirect('/players')
        # except:
        #     return "Ошибка при обновлении базы данных"
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
        print(player1+" "+player2+" "+player3+" "+player4+" "+player5+" "+player6)

        act.start_info_update_players(player1+" "+player2+" "+player3+" "+player4+" "+player5+" "+player6)

        # article = Article(name=player1+" "+player2+" "+player3+" "+player4+" "+player5+" "+player6,
        #                   smth2="Игроки")
        # try:
        #     db.session.add(article)
        #     db.session.commit()
        #     print("edited")
        #     return redirect('/the_game')
        # except:
        #     return "Ошибка при обновлении базы данных"

        return redirect('/the_game')

    else:
        return render_template("players_page.html")


@app.route('/the_game')
def the_game():
    return render_template("the_game.html")


if __name__ == "__main__":
    act = WEB_Replies()
    app.run(debug=True)