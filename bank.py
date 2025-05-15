
class Account:
    def __init__(self, username, password, balance):
        self.username = username
        self.password = password
        self.balance = self.to_twos_complement(balance)

    def to_twos_complement(self, value):
        if value < 0:
            value = (1 << 32) + value
        return value

    def to_decimal(self):
        if self.balance & (1 << 31):
            return self.balance - (1 << 32)
        return self.balance

    def update_balance(self, amount):
        new_balance = self.to_decimal() + amount
        self.balance = self.to_twos_complement(new_balance)


accounts = {}


def store_account_details(username, password, initial_deposit):
    accounts[username] = Account(username, password, initial_deposit)


def verify_account_details(username, password):
    return username in accounts and accounts[username].password == password


def get_balance(username):
    return accounts[username].balance


def convert_to_decimal(twos_complement_value):
    if twos_complement_value & (1 << 31):
        return twos_complement_value - (1 << 32)
    return twos_complement_value


def update_balance(username, amount):
    accounts[username].update_balance(amount)


def create_account():
    print("---- Create New Account ----")
    username = input("Enter username: ")
    if username in accounts:
        print("Username already exists.")
        return

    password = input("Enter password (8–16 characters): ")
    while len(password) < 8 or len(password) > 16:
        print("Password must be 8 to 16 characters")
        password = input("Re-enter password: ")

    try:
        initial_deposit = float(input("Enter initial deposit amount: £"))
        if initial_deposit < 0:
            print("Invalid amount")
            return
    except ValueError:
        print("Invalid input.")
        return

    store_account_details(username, password, initial_deposit)
    print("Account created successfully ^^")
    banking_menu(username)


def login():
    print("---- Account Login ----")
    login_attempts = 0
    max_login_attempts = 3

    while login_attempts < max_login_attempts:
        username = input("Username: ")
        password = input("Password: ")

        if verify_account_details(username, password):
            print("Login successful.")
            banking_menu(username)
            return
        else:
            login_attempts += 1
            print("Invalid username or password. Try again.")

    print("Too many incorrect attempts. Account locked")


def check_balance(account_name):
    balance_2s = get_balance(account_name)
    balance_decimal = convert_to_decimal(balance_2s)
    print(f"Your current balance is: £{balance_decimal:.2f}")


def deposit(account_name):
    try:
        deposit_amount = float(input("Enter amount to deposit: £"))
        if deposit_amount <= 0:
            print("Invalid deposit amount.")
            return
        update_balance(account_name, deposit_amount)
        print("Deposit successful.")
    except ValueError:
        print("Invalid input.")


def withdraw(account_name):
    try:
        withdraw_amount = float(input("Enter amount to withdraw: £"))
        balance = convert_to_decimal(get_balance(account_name))

        if withdraw_amount <= balance or (balance - withdraw_amount) >= -1500:
            update_balance(account_name, -withdraw_amount)
            print("Withdrawal successful.")
        else:
            print("Insufficient funds.")
    except ValueError:
        print("Invalid input.")


def transfer(from_account):
    to_account = input("Enter account to transfer to: ")
    if to_account not in accounts:
        print("Recipient account not found.")
        return

    try:
        transfer_amount = float(input("Enter amount to transfer: £"))
        from_balance = convert_to_decimal(get_balance(from_account))

        if transfer_amount <= from_balance or (from_balance - transfer_amount) >= -1500:
            update_balance(from_account, -transfer_amount)
            update_balance(to_account, transfer_amount)
            print("Transfer successful.")
        else:
            print("Insufficient funds for transfer.")
    except ValueError:
        print("Invalid input.")


def banking_menu(account_name):
    while True:
        print("\n---- Menu ----")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Exit")

        choice = input("Enter option: ")

        if choice == '1':
            check_balance(account_name)
        elif choice == '2':
            deposit(account_name)
        elif choice == '3':
            withdraw(account_name)
        elif choice == '4':
            transfer(account_name)
        elif choice == '5':
            print("Logging out…")
            break
        else:
            print("Invalid option. Try again.")


def main():
    print("Welcome to the bank application")
    while True:
        print("\n1. New Account")
        print("2. Login to Existing Account")
        print("3. Exit")

        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            create_account()
        elif user_choice == '2':
            login()
        elif user_choice == '3':
            print("Exiting Application")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


