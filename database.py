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

class AddInData:
    def __init__(self, account_name, balance):
        self.account_name = account_name
        self.balance = balance

    def save_to_db(self):
        cursor.execute(
            "INSERT INTO accounts(account_name, balance) VALUES(?, ?)",
            (self.account_name, self.balance)
        )
        connection.commit()

class GetInAcc(AddInData):
    def __init__(self):
        super().__init__(account_name=None, balance=None)
    def get_all_acc(self):
        cursor.execute('SELECT * FROM accounts')
        return cursor
    connection.commit()

class AddInCategory:
    def __init__(self, account_id, category_name, type):
        self.account_id = account_id
        self.category_name = category_name
        self.type = type
    def save_to_db(self):
        cursor.execute(
            "INSERT INTO categories(id_account,name, type) VALUES(?,?,?)",(self.account_id,self.category_name, self.type)
        )
        connection.commit()

class GetInCategory(AddInCategory):
    def __init__(self):
        super().__init__(account_id=None,category_name=None, type=None)
    def get_categories_id_account(self):
        cursor.execute('SELECT id,name, type FROM categories WHERE id_account=?',(self.account_id,))
        return cursor
    def get_all_category(self):
        cursor.execute('SELECT * FROM categories')
        return cursor
    connection.commit()

class Transaction:
    def __init__(self, account_id, category_id, amount, description, date):
        self.account_id = account_id
        self.category_id = category_id
        self.amount = amount
        self.description = description
        self.date = date
    def add_transaction(self):
        cursor.execute(
            'SELECT type FROM categories WHERE id = ?',
            (self.category_id,))

        category_type = cursor.fetchone()[0]

        cursor.execute(
            'INSERT INTO transactions(account_id, category_id, amount, description, date) VALUES(?,?,?,?,?)',
            (self.account_id, self.category_id, self.amount, self.description, self.date)
        )

        if category_type == 'income':
            cursor.execute('''
                UPDATE accounts 
                SET balance = balance + ?
                WHERE id = ?
                                 ''',(self.amount, self.account_id)
            )
        elif category_type == 'expense':
            cursor.execute('''
            UPDATE accounts 
            SET balance = balance - ?
            WHERE id = ?    
            ''', (self.amount,self.account_id)
            )
        connection.commit()
        print('☑️The transaction was successful.')
    def search_transaction(self):
        cursor.execute('''
            SELECT
                transactions.amount,
                transactions.description,
                transactions.date,
                accounts.account_name,
                categories.name AS category_name
            FROM transactions
            JOIN accounts ON transactions.account_id = accounts.id
            JOIN categories ON transactions.category_id = categories.id
            WHERE accounts.id = ? AND transactions.category_id = ?
        ''', (self.account_id, self.category_id))


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
                "DELETE FROM categories WHERE id_account = ?",
                (self.account_id,)
            )
            cursor.execute(
                "DELETE FROM accounts WHERE id = ?",
                (self.account_id,)
            )
        elif self.category_id is not None:
            cursor.execute(
                "DELETE FROM categories WHERE id = ?",
                (self.category_id,)
            )
        connection.commit()


