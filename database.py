import sqlite3

Connection = sqlite3.connect('accounts.db')
cursor = Connection.cursor()

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

Connection.commit()

class AddInData:
    def __init__(self, account_name, balance):
        self.account_name = account_name
        self.balance = balance

    def save_to_db(self):
        cursor.execute(
            "INSERT INTO accounts(account_name, balance) VALUES(?, ?)",
            (self.account_name, self.balance)
        )
        Connection.commit()

class AddInCategory:
    def __init__(self, category_name, type):
        self.category_name = category_name
        self.type = type
    def save_to_db(self):
        cursor.execute(
            "INSERT INTO categories(name, type) VALUES(?, ?)",(self.category_name, self.type)
        )
        Connection.commit()

class Transaction:
    def __init__(self, account_id, category_id, amount, description, date):
        self.account_id = account_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        self.date = date

class GetInAcc:
    def __init__(self):
        pass
    def get_all_acc(self):
        cursor.execute('SELECT * FROM accounts')
        return cursor
    Connection.commit()

class DeleteInData:
    def __init__(self, account_id, category_id):
        self.account_id = account_id
        self.category_id = category_id
    def delete_from_db(self):
        if self.account_id is not None:
            cursor.execute(
                "UPDATE transactions SET account_id = NULL WHERE account_id = ?",
                (self.account_id,)
            )
            cursor.execute(
                "DELETE FROM accounts WHERE id = ?",
                (self.account_id,)
            )
        elif self.category_id is not None:
            cursor.execute(
                "DELETE FROM categories WHERE id = ?", (self.category_id,)
            )

    Connection.commit()

