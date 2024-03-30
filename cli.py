from models import User, BudgetAccount, Transaction, engine, Base
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt
import getpass
import sys

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

current_user = None

def login():
    global current_user
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.verify(password, user.password_hash):
        print("Login successful.")
        current_user = user
    else:
        print("Invalid username or password.")

def register():
    name = input("Enter your name: ")
    username = input("Choose a username: ")
    password = getpass.getpass("Choose a password: ")

    hashed_password = bcrypt.hash(password)
    new_user = User(name=name, username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()
    print("Registration successful.")

def view_main_account_balance():
    if current_user:
        print(f"Main Account Balance: {current_user.main_account_balance}")
    else:
        print("No user logged in.")

def deposit_to_main_account():
    if current_user:
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            current_user.main_account_balance += amount
            session.commit()
            print("Deposit successful.")
        else:
            print("Invalid amount.")
    else:
        print("No user logged in.")

def withdraw_from_main_account():
    if current_user:
        amount = float(input("Enter amount to withdraw: "))
        if 0 < amount <= current_user.main_account_balance:
            current_user.main_account_balance -= amount
            session.commit()
            print("Withdrawal successful.")
        else:
            print("Invalid amount or insufficient balance.")
    else:
        print("No user logged in.")

def create_budget_account():
    if current_user:
        name = input("Enter the name for your new budget account: ")
        new_account = BudgetAccount(name=name, user=current_user)
        session.add(new_account)
        session.commit()
        print("Budget account created successfully.")
    else:
        print("No user logged in.")

def view_budget_accounts():
    if current_user:
        print("Budget Accounts:")
        for account in current_user.budget_accounts:
            print(f"ID: {account.id}, Name: {account.name}, Balance: {account.balance}")
    else:
        print("No user logged in.")

def deposit_to_budget_account():
    if current_user:
        view_budget_accounts()
        account_id = int(input("Enter the ID of the budget account to deposit into: "))
        amount = float(input("Enter amount to deposit: "))
        account = session.query(BudgetAccount).filter_by(id=account_id).first()
        if account:
            if amount > 0 and current_user.main_account_balance >= amount:
                current_user.main_account_balance -= amount
                account.balance += amount
                session.commit()
                print("Deposit successful.")
            else:
                print("Invalid amount or insufficient balance.")
        else:
            print("Budget account not found.")
    else:
        print("No user logged in.")

def withdraw_from_budget_account():
    if current_user:
        view_budget_accounts()
        account_id = int(input("Enter the ID of the budget account to withdraw from: "))
        amount = float(input("Enter amount to withdraw: "))
        account = session.query(BudgetAccount).filter_by(id=account_id).first()
        if account:
            if 0 < amount <= account.balance:
                current_user.main_account_balance += amount
                account.balance -= amount
                session.commit()
                print("Withdrawal successful.")
            else:
                print("Invalid amount or insufficient balance.")
        else:
            print("Budget account not found.")
    else:
        print("No user logged in.")

def transfer_between_budget_accounts():
    if current_user:
        view_budget_accounts()
        from_account_id = int(input("Enter the ID of the source budget account: "))
        to_account_id = int(input("Enter the ID of the destination budget account: "))
        amount = float(input("Enter amount to transfer: "))

        from_account = session.query(BudgetAccount).filter_by(id=from_account_id).first()
        to_account = session.query(BudgetAccount).filter_by(id=to_account_id).first()

        if from_account and to_account:
            if 0 < amount <= from_account.balance:
                from_account.balance -= amount
                to_account.balance += amount
                session.commit()
                print("Transfer successful.")
            else:
                print("Invalid amount or insufficient balance.")
        else:
            print("One or both of the budget accounts not found.")
    else:
        print("No user logged in.")

def delete_budget_account():
    if current_user:
        view_budget_accounts()
        account_id = int(input("Enter the ID of the budget account to delete: "))
        account = session.query(BudgetAccount).filter_by(id=account_id).first()
        if account:
            current_user.main_account_balance += account.balance
            session.delete(account)
            session.commit()
            print("Budget account deleted successfully.")
        else:
            print("Budget account not found.")
    else:
        print("No user logged in.")

def logout():
    global current_user
    current_user = None
    print("Logout successful.")

def exit_application():
    print("Exiting the application. Goodbye!")
    sys.exit()

def main_menu():
    print("\nMain Menu:")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

def user_menu():
    print("\nUser Menu:")
    print("1. View Main Account Balance")
    print("2. Deposit to Main Account")
    print("3. Withdraw from Main Account")
    print("4. Create Budget Account")
    print("5. View Budget Accounts")
    print("6. Deposit to Budget Account")
    print("7. Withdraw from Budget Account")
    print("8. Transfer between Budget Accounts")
    print("9. Delete Budget Account")
    print("10. Logout")
    print("11. Exit")

def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            login()
        elif choice == '2':
            register()     
        elif choice == '3':
            exit_application()
        else:
            print("Invalid choice. Please try again.")

        if current_user:
            while True:
                user_menu()
                choice = input("Enter your choice: ")

                if choice == '1':
                    view_main_account_balance()
                elif choice == '2':
                    deposit_to_main_account()
                elif choice == '3':
                    withdraw_from_main_account()
                elif choice == '4':
                    create_budget_account()
                elif choice == '5':
                    view_budget_accounts()
                elif choice == '6':
                    deposit_to_budget_account()
                elif choice == '7':
                    withdraw_from_budget_account()
                elif choice == '8':
                    transfer_between_budget_accounts()
                elif choice == '9':
                    delete_budget_account()
                elif choice == '10':
                    logout()
                    break
                elif choice == '11':
                    exit_application()
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
