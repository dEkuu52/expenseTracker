import database
import matplotlib
from prettytable import from_db_cursor
from datetime import datetime



# ----------- Main func -----------
def main_func():
    welcome_message()

    choice = input('Enter the number of the function you need: ')

    if choice == '1':
        create_new_acc()
    elif choice == '2':
        add_category()
    elif choice == '3':
        get_acc()
    elif choice == '4':
        add_trans()
    elif choice =='6':
        delete_acc()


# ----------- Welcome func -----------
def welcome_message():
    try:
        with open('welcome_message', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print('File not found')


# ------------ 1. Create acc func ------------
def create_new_acc():
    all_entries = {}

    while True:
        name = input('Enter your account name: ')
        try:
            balance = float(input('Enter your account balance: '))
        except ValueError:
            print('Please enter a valid number')
            continue

        print('Your account has been created.')

        new_entry = database.AddInData(account_name=name, balance=balance)
        new_entry.save_to_db()

        all_entries[name, balance] = new_entry
        break
    return all_entries

# ------------ 2. Add category func ------------
def add_category():
    all_category_entries = {}

    while True:
        # get_acc
        db_cursor_acc = database.GetInAcc().get_all_acc()
        print(from_db_cursor(db_cursor_acc))

        account_id = input('Enter your account id(or "Exit"): ')
        if account_id.strip().lower() == 'exit':
            print("Returning to main menu...")
            main_func()

        category_name = input('Enter your category name: ')

        if category_name.strip().lower() == 'exit':
            print("Returning to main menu...")
            main_func()

        type_category = input('Enter your category type (Indicate here whether this is "income" or an "expense"): ')

        if type_category.strip().lower() == 'exit':
            print("Returning to main menu...")
            main_func()
        print('Once you have added all the categories you need, you can enter "Exit" to return to the main menu.')

        new_entry = database.AddInCategory(
            account_id=int(account_id),
            category_name=category_name,
            type=type_category,
        )
        new_entry.save_to_db()
        all_category_entries[category_name] = new_entry

# ------------ 3. Get acc func ------------
def get_acc():
    db_cursor = database.GetInAcc().get_all_acc()
    print(from_db_cursor(db_cursor))
    db_cursor_cat = database.GetInCategory().get_all_category()
    print(from_db_cursor(db_cursor_cat))

# ------------ 4. Transactions ------------
def add_trans():
    account_id = int(input("Enter account ID: "))
    category_id = int(input("Enter the category ID: "))
    amount = float(input("Enter the amount: "))
    description = input("Enter a description: ")
    date = input("Enter the date (YYYY-MM-DD) or press Enter for the current date: ")

    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    tx_obg = database.Transaction(account_id, category_id, amount, description, date)
    tx_obg.add_transaction()



# ------------ 6. Delete acc ------------
def delete_acc():
    get_acc()
    selected_acc = input('Enter the id of the account you want to delete: ')

    id_delete_db = int(selected_acc)

    deleter = database.DeleteInData(account_id=id_delete_db, category_id=None)
    deleter.delete_from_db()
    print('Account has been deleted.')


if __name__ == "__main__":
    main_func()