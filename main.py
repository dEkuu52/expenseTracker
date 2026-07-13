import database
import matplotlib
from prettytable import from_db_cursor


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


# ----------- Welcome func -----------
def welcome_message():
    try:
        with open('welcome_message', 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print('File not found')


# ------------ Create acc func ------------
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


# ------------ Get acc func ------------
def get_acc():
    db_cursor = database.GetInAcc().get_all_acc()
    print(from_db_cursor(db_cursor))


# ------------ Add category func ------------
def add_category():
    all_category_entries = {}

    while True:
        category_name = input('Enter your category name: ')

        if category_name.strip().lower() == 'exit':
            print("Returning to main menu...")
            main_func()

        type_category = input('Enter your category type: ')
        print('Once you have added all the categories you need, you can enter "Exit" to return to the main menu.')

        new_entry = database.AddInCategory(category_name=category_name, type=type_category)
        new_entry.save_to_db()
        all_category_entries[category_name] = new_entry


# ------------ Delete acc ------------
def delete_acc():
    get_acc()
    selected_acc = input('Enter the number of the account you want to delete: ')


if __name__ == "__main__":
    main_func()