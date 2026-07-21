import models
import matplotlib
from prettytable import from_db_cursor
from datetime import datetime



# ----------- Main func -----------
def main_func():
    welcome_message()

    choice = input('Enter the number of the function you need(If you want to exit, enter "Exit"): ')

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
    elif choice.strip().lower() == 'Exit':
        exit()


# ----------- Welcome func -----------
def welcome_message():
    try:
        with open('welcome_message', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print('❌ File not found')


# ------------ 1. Create acc func ------------
def create_new_acc():
    all_entries = {}

    while True:
        name = input('Enter your account name(If you want to exit, enter "Exit"): ')
        try:
            balance = float(input('Enter your account balance: '))
        except ValueError:
            print('Please enter a valid number')
            continue

        print('☑️ Your account has been created.')

        new_entry = models.AddInData(account_name=name, balance=balance)
        new_entry.save_to_db()

        all_entries[name, balance] = new_entry

        if name or balance == 'Exit':
            print("🕗 Returning to main menu...")
            main_func()
            break
    return all_entries


# ------------ 2. Add category func ------------
def add_category():
    all_category_entries = {}

    while True:
        # get_acc
        db_cursor_acc = models.GetInAcc().get_all_acc()
        print(from_db_cursor(db_cursor_acc))

        account_id = input('Enter your account id(or "Exit"): ')
        if account_id.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
            break

        category_name = input('Enter your category name: ')

        if category_name.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
            break

        type_category = input('Enter your category type (Indicate here whether this is "income" or an "expense"): ')

        if type_category.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
        print('Once you have added all the categories you need, you can enter "Exit" to return to the main menu.')

        new_entry = models.AddInCategory(
            account_id=int(account_id),
            category_name=category_name,
            type=type_category,
        )
        new_entry.save_to_db()
        all_category_entries[category_name] = new_entry

# ------------ 3. Get acc func ------------
def get_acc():
    while True:
        db_cursor = models.GetInAcc().get_all_acc()
        print(from_db_cursor(db_cursor))
        db_cursor_cat = models.GetInCategory().get_all_category()
        print(from_db_cursor(db_cursor_cat))

        choice = input('If you want to exit, enter "Exit": ')
        if choice.strip().lower() == 'Exit':
            print("🕗 Returning to main menu...")
            main_func()


def get_acc_for_del():
    db_cursor = models.GetInAcc().get_all_acc()
    print(from_db_cursor(db_cursor))
    db_cursor_cat = models.GetInCategory().get_all_category()
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

    tx_obg = models.Transaction(account_id, category_id, amount, description, date)
    tx_obg.add_transaction()



# ------------ 6. Delete acc ------------
def delete_acc():
    while True:
        get_acc_for_del()
        selected_acc = input('Enter the id of the account you want to delete(If you want to exit, enter "Exit"): ')

        id_delete_db = int(selected_acc)

        deleter = models.DeleteInData(account_id=id_delete_db, category_id=None)
        deleter.delete_from_db()
        print('☑️ Account has been deleted.')

        if  selected_acc or id_delete_db == 'Exit':
            print("🕗 Returning to main menu...")
            main_func()


if __name__ == "__main__":
    main_func()