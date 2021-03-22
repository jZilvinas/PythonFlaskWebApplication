import sqlite3
import json

connection = sqlite3.connect('games.db')

g = connection.cursor()

with open('gamesData.json', encoding='utf-8-sig') as file:
    data = json.loads(file.read())

games = []

for i in data['Games']:
    games.append((i['name'], i['genre'], i['platform'], i['price'], i['release_date'], i['availability'], i['pegi']))

g.execute('''
    CREATE TABLE games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100),
        genre VARCHAR(100),
        platform VARCHAR(100),
        price DECIMAL,
        release_date VARCHAR(100),
        availability VARCHAR(100),
        pegi VARCHAR(100)
    )''')

g.executemany('''
    INSERT INTO games (name, genre, platform, price, release_date, availability, pegi)
    VALUES (?, ?, ?, ?, ?, ?,?)
''', games)

g.execute('''SELECT name, price FROM games''')
connection.commit()
table_rows = g.fetchall()
for row in table_rows:
    print(row)


g.close()
connection.close()