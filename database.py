import sqlite3

connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()

cursor.execute('''
PRAGMA foreign_keys = ON;
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_name TEXT,
    balance REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_account INTEGER,
    name TEXT,
    type TEXT,
    FOREIGN KEY (id_account) REFERENCES accounts(id))
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    category_id INTEGER,
    amount REAL,
    description TEXT,
    date DATETIME,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')
connection.commit()




