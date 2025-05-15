import json
import os

DATA_FILE = "accounts.json"

class BankAccount:
    def __init__(self, username, password, balance, already_in_pennies=False):
        
        self.username = username
        self.password = password
        if already_in_pennies:
            self.balance = self.to_twos_complement(balance)
        else:
            self.balance = self.to_twos_complement(int(round(balance * 100)))


    def to_twos_complement(self, n):
        if n < 0:
            return (1 << 32) + n
        return n

    def from_twos_complement(self):
        n = int(self.balance)
        if n & (1 << 31):
            n= n - (1 << 32)
        return n/100

    def deposit(self, amount):
        current = self.from_twos_complement()
        new_total = current + amount
        self.balance = self.to_twos_complement(int(round(new_total * 100)))


    def withdraw(self, amount):
        current = self.from_twos_complement()
        if current - amount >= -1500:
            new_total = current - amount
            self.balance = self.to_twos_complement(int(round(new_total * 100)))
            return True
        return False


    def transfer(self, amount, other_account):
        if self.withdraw(amount):
            other_account.deposit(amount)
            return True
        return False

class BankingSystem:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)
            return {
                user: BankAccount(user, data["password"], int(data["balance"]),already_in_pennies=True)
                for user, data in raw.items()
            }

    def save_accounts(self):
        data = {user: {"password": acc.password, "balance": acc.balance}
                for user, acc in self.accounts.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    def from_twos_complement(self, n):
        if n & (1 << 31):
            return n - (1 << 32)
        return n

    def create_account(self):
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

        self.accounts[username] = BankAccount(username, password, initial_deposit)
        self.save_accounts()
        print("Account created successfully ^^")

    def login(self):
        print("\n---- Account Login ----")
        attempts = 0
        while attempts < 3:
            username = input("Enter username: ")
            password = input("Enter password: ")

            account = self.accounts.get(username)
            if account and account.password == password:
                print("Login successful.")
                self.banking_menu(account)
                return
            else:
                attempts += 1
                print("Invalid username or password.")

        print("Too many incorrect attempts. Account locked.")

    def banking_menu(self, account):
        while True:
            print("\n---- Menu ----")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. Exit")

            choice = input("Choose an option: ")
            if choice == "1":
                print(f"Your current balance is: £{account.from_twos_complement()}")
            elif choice == "2":
                try:
                    amount = float(input("Enter amount to deposit: £"))
                    if amount <= 0:
                        print("Invalid deposit amount.")
                    else:
                        account.deposit(amount)
                        self.save_accounts()
                        print("Deposit successful.")
                except ValueError:
                    print("Invalid input.")
            elif choice == "3":
                try:
                    amount = float(input("Enter amount to withdraw: £"))
                    if account.withdraw(amount):
                        self.save_accounts()
                        print("Withdrawal successful.")
                    else:
                        print("Insufficient funds.")
                except ValueError:
                    print("Invalid input.")
            elif choice == "4":
                to_user = input("Enter account to transfer to: ")
                if to_user not in self.accounts:
                    print("Account does not exist.")
                    continue
                try:
                    amount = float(input("Enter amount to transfer: £"))
                    if account.transfer(amount, self.accounts[to_user]):
                        self.save_accounts()
                        print("Transfer successful.")
                    else:
                        print("Insufficient funds for transfer.")
                except ValueError:
                    print("Invalid amount.")
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid option. Try again.")

    def main_menu(self):
        print("Welcome to the bank Application")
        while True:
            print("\nMain Menu:")
            print("1. Create New Account")
            print("2. Login to Existing Account")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = BankingSystem()
    app.main_menu()