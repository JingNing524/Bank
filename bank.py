
import json
import os




DATA_FILE = "accounts.json"





def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(DATA_FILE, "w") as f:
        json.dump(accounts, f)





def to_twos_complement(n):
    if n < 0:
        return (1 << 32) + n
    return n

def from_twos_complement(n):
    if n & (1 << 31):
        return n - (1 << 32)
    return n





def create_account(accounts):
    print("\n---- Create New Account ----")
    username = input("Enter username: ")
    
    while True:
        password = input("Enter password (8–16 characters): ")
        if 8 <= len(password) <= 16:
            break
        print("Password must be 8 to 16 characters.")

    try:
        initial_deposit = float(input("Enter initial deposit: £"))
        if initial_deposit < 0:
            print("Invalid amount.")
            return
    except ValueError:
        print("Invalid amount format.")
        return

    accounts[username] = {
        "password": password,
        "balance": to_twos_complement(int(initial_deposit))
    }
    save_accounts(accounts)
    print("Account created successfully ^^")

def login(accounts):
    print("\n---- Account Login ----")
    attempts = 0
    while attempts < 3:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in accounts and accounts[username]["password"] == password:
            print("Login successful.")
            banking_menu(username, accounts)
            return
        else:
            attempts += 1
            print("Invalid username or password.")

    print("Too many incorrect attempts. Account locked.")



def banking_menu(username, accounts):
    while True:
        print("\n---- Menu ----")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            check_balance(username, accounts)
        elif choice == "2":
            deposit(username, accounts)
        elif choice == "3":
            withdraw(username, accounts)
        elif choice == "4":
            transfer(username, accounts)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")



def check_balance(username, accounts):
    balance_twos = accounts[username]["balance"]
    balance = from_twos_complement(balance_twos)
    print(f"Your current balance is: £{balance}")

def deposit(username, accounts):
    try:
        amount = float(input("Enter amount to deposit: £"))
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        current = from_twos_complement(accounts[username]["balance"])
        new_balance = current + amount
        accounts[username]["balance"] = to_twos_complement(int(new_balance))
        save_accounts(accounts)
        print("Deposit successful.")
    except ValueError:
        print("Invalid input.")

def withdraw(username, accounts):
    try:
        amount = float(input("Enter amount to withdraw: £"))
        current = from_twos_complement(accounts[username]["balance"])
        if current - amount >= -1500:
            new_balance = current - amount
            accounts[username]["balance"] = to_twos_complement(int(new_balance))
            save_accounts(accounts)
            print("Withdrawal successful.")
        else:
            print("Insufficient funds.")
    except ValueError:
        print("Invalid input.")

def transfer(from_user, accounts):
    to_user = input("Enter account to transfer to: ")
    if to_user not in accounts:
        print("Account does not exist.")
        return

    try:
        amount = float(input("Enter amount to transfer: £"))
        sender_balance = from_twos_complement(accounts[from_user]["balance"])

        if sender_balance - amount >= -1500:
            accounts[from_user]["balance"] = to_twos_complement(int(sender_balance - amount))
            receiver_balance = from_twos_complement(accounts[to_user]["balance"])
            accounts[to_user]["balance"] = to_twos_complement(int(receiver_balance + amount))
            save_accounts(accounts)
            print("Transfer successful.")
        else:
            print("Insufficient funds for transfer.")
    except ValueError:
        print("Invalid amount.")




def main():
    accounts = load_accounts()
    print("Welcome to the bank Application")
    while True:
        print("\nMain Menu:")
        print("1. Create New Account")
        print("2. Login to Existing Account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            login(accounts)
        elif choice == "3":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()