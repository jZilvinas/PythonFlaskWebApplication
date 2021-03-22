from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DataBase configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'

db = SQLAlchemy(app)


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, db.Sequence("seq_street_segment_id"), primary_key = 'true')
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100), nullable=False)
    pegi = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)

@app.route('/game/<int:id>')
def gameInfo(id):
    games = Game.query.get_or_404(id)
    return render_template('gameInfo.html', game=games)

@app.route('/addgame', methods = ['GET', 'POST'])
def addGame():
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']
        platform = request.form['platform']
        price = request.form['price']
        release_date = request.form['release_date']
        availability = request.form['availability']
        pegi = request.form['pegi']
        newGame = Game(name=name, genre=genre, platform=platform, price=price, release_date=release_date, availability=availability, pegi=pegi)
        try:
            db.session.add(newGame)
            db.session.commit()
            return redirect('/')
        except:
            return 'Item was not added due to some issues.'

    return render_template('addGame.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    game = Game.query.get_or_404(id)

    if request.method == 'POST':
        game.name = request.form['name']
        game.genre = request.form['genre']
        game.platform = request.form['platform']
        game.price= request.form['price']
        game.release_date = request.form['release_date']
        game.availability = request.form['availability']
        game.pegi = request.form['pegi']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Game was not updated due to some issues."
    else:
        return render_template('update.html', game=game)


@app.route('/delete/<int:id>')
def delete(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect('/')


@app.route('/search', methods=['GET','POST'])
def search ():
    if request.method=='POST':
        search_value = request.form['search_string']    
        print(search_value)
        search = "%{0}%".format(search_value)
        results = Game.query.filter(Game.name.like(search)).all()
        return render_template('index.html', games = results)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)