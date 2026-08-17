import models
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
    elif choice == '5':
        all_transaction()
    elif choice == '6':
        annual_exp()
    elif choice =='7':
        delete_acc()
    elif choice.strip().lower() == 'exit':
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
        if name.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
            break
        try:
            balance = float(input('Enter your account balance: '))
        except ValueError:
            print('Please enter a valid number')
            continue

        print('☑️ Your account has been created.')

        new_entry = models.AddInData(account_name=name, balance=balance)
        new_entry.save_to_db()

        all_entries[name, balance] = new_entry


# ------------ 2. Add category func ------------
def add_category():
    all_category_entries = {}

    while True:
        # get_acc
        db_cursor_acc = models.GetInAcc().get_all_acc()
        print(from_db_cursor(db_cursor_acc))

        print(' 🔙 If you want to return to the main menu, enter "Exit" ')

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
            break
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
        if choice.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
            break


def get_acc_for_del():
    db_cursor = models.GetInAcc().get_all_acc()
    print(from_db_cursor(db_cursor))
    db_cursor_cat = models.GetInCategory().get_all_category()
    print(from_db_cursor(db_cursor_cat))

# ------------ 4. Transactions ------------
def add_trans():
    while True:
        print(' If you want to return to the main menu, enter "Exit" ')

        account_input = input('Enter your account id(or "Exit"): ')
        if account_input.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
            break

        try:
            account_id = int(account_input)
            category_id = int(input("Enter the category ID: "))
            amount = float(input("Enter the amount: "))
        except ValueError:
            print("❌ Error: ID and amount must be numbers! Please try again.")
            continue

        description = input("Enter a description: ")
        date = input("Enter the date (DD-MM-YYYY) or press Enter for current date: ").strip()

        if not date:
            date = datetime.today().strftime('%d-%m-%Y')

        try:
            tx_obg = models.Transaction(
                account_id,
                category_id,
                amount,
                description,
                date)
            tx_obg.add_transaction()
            print('☑️The transaction was successful.')
        except Exception as e:
            print(f'❌ Failed to save the transaction: {e}')
            continue

# ------------ 5. All Transactions ------------
def all_transaction():
    while True:
        choice_acc_id = input('Enter your account id(or "Exit"): ')
        if choice_acc_id.strip().lower() == 'exit':
            print("🕗 Returning to main menu...")
            main_func()
            break

        try:
            choice_id = int(choice_acc_id)
        except ValueError:
            print('Please enter a valid number')
            continue

        trans_all = models.Transaction(account_id=choice_id, category_id=None,amount=0, description=None, date=None)
        transct_acc = trans_all.search_transaction()

        if not transct_acc:
            print(f'❌ No transactions found for this {choice_acc_id}.')
        print(from_db_cursor(transct_acc))

# ------------ 6.Annual expenses ------------
def annual_exp():
    while True:
        print(' If you want to return to the main menu, enter "Exit"')
        choice_date1 = input('Enter the start date (DD-MM-YYYY): ')
        choice_date2 = input('Enter the end date (DD-MM-YYYY): ')

        if choice_date1.strip().lower() == 'exit':
            main_func()
            break

        if choice_date2.strip().lower() == 'exit':
            main_func()
            break

        x = models.GraphMonth(date_1=choice_date1, date_2=choice_date2)

        data_gr = x.show_graph()
        print(data_gr)


# ------------ 7. Delete acc ------------
def delete_acc():
    while True:
        get_acc_for_del()
        selected_acc = input('Enter the id of the account you want to delete(If you want to exit, enter "Exit"): ')

        id_delete_db = int(selected_acc)

        deleter = models.DeleteInData(account_id=id_delete_db, category_id=None)
        deleter.delete_from_db()
        print('☑️ Account has been deleted.')

        if  selected_acc.strip().lower() == 'Exit':
            print("🕗 Returning to main menu...")
            main_func()


if __name__ == "__main__":
    main_func()