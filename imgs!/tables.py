import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            email TEXT,
            password TEXT,
            like_imgs TEXT
            )''')
cur.execute('''CREATE TABLE IF NOT EXISTS imgs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img TEXT,
            discribe TEXT,
            likes INTEGER,
            comments INTEGER,
            users_like TEXT
            )''')
cur.execute('''CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img TEXT,
            text TEXT,
            nickname TEXT,
            data TEXT
            )''')
cur.execute('''CREATE TABLE IF NOT EXISTS test_generate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img TEXT,
            text TEXT
            )''')
# cur.execute('DROP TABLE imgs')
# cur.execute('UPDATE imgs SET users_like = ? WHERE id = ?', ['', 1])
conn.commit()