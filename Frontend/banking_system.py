from session import Session
from bank_accounts import BankAccounts
from transaction_executor import TransactionExecutor
from transaction_file_writer import TransactionFileWriter


class BankingSystem:
    def __init__(self):
        self.session = None
        self.accounts = BankAccounts()
        self.executor = TransactionExecutor(self.accounts)
        self.writer = TransactionFileWriter()

    def run(self):
        print("Banking System\n")
        self.login()
        self.accounts.load_accounts("current_bank_accounts.txt")

        while self.session.is_active:
            if self.session.user_type == "SU":
                self.display_standard_menu()
            else:
                self.display_admin_menu()

        self.logout()

    def login(self):
        print("Login Menu\nStandard User: SU\nAdmin User: AU\n")
        user_type = self.prompt_user_type()

        if user_type == "SU":
            username = self.prompt_username()
            self.session = Session(user_type="SU", username=username, is_active=True)
        else:
            self.session = Session(user_type="AU", username="", is_active=True)

    def display_standard_menu(self):
        print(
            "\nStandard User Menu\nDeposit: DP\nWithdrawal: WD\nTransfer: TR\nPay Bill: PB\nLogout: LO\n"
        )
        transaction_code = self.prompt_transaction_code()
        self.handle_transaction(transaction_code)

    def display_admin_menu(self):
        print(
            "\nAdmin User Menu\nDeposit: DP\nWithdrawal: WD\nTransfer: TR\nPay Bill: PB\nCreate Account: CA\nDelete Account: DE\nDisable Account: DI\nChange Account Plan: CP\nLogout: LO\n"
        )
        transaction_code = self.prompt_transaction_code()
        self.handle_transaction(transaction_code)

    def handle_transaction(self, transaction_code):
        if transaction_code == "DP":
            transaction_record = self.executor.execute_deposit(self.session)
        elif transaction_code == "WD":
            transaction_record = self.executor.execute_withdrawal(self.session)
        elif transaction_code == "TR":
            transaction_record = self.executor.execute_transfer(self.session)
        elif transaction_code == "PB":
            transaction_record = self.executor.execute_pay_bill(self.session)
        elif transaction_code == "CA":
            transaction_record = self.executor.execute_create_account(self.session)
        elif transaction_code == "DE":
            transaction_record = self.executor.execute_delete_account(self.session)
        elif transaction_code == "DI":
            transaction_record = self.executor.execute_disable_account(self.session)
        elif transaction_code == "CP":
            transaction_record = self.executor.execute_change_account_plan(self.session)
        elif transaction_code == "LO":
            self.session.is_active = False
            return
        else:
            print("Invalid transaction code.")

        if transaction_record:
            print("Transaction completed.")
            self.writer.write_transaction_record(transaction_record)

    def logout(self):
        transaction_record = self.executor.execute_logout()
        if transaction_record:
            self.writer.write_transaction_record(transaction_record)

        print("Logout completed.")

    def prompt_user_type(self):
        while True:
            user_type = input("Enter user type: ").strip().upper()
            if user_type in ["SU", "AU"]:
                return user_type
            else:
                print("Invalid user type.")

    def prompt_username(self):
        while True:
            username = input("Enter account holder name: ").strip().title()
            if 1 <= len(username) <= 20:
                return username
            else:
                print("Invalid username: Must be 1-20 characters.")

    def prompt_transaction_code(self):
        while True:
            transaction_code = input("Enter transaction code: ").strip().upper()
            if transaction_code in [
                "DP",
                "WD",
                "TR",
                "PB",
                "CA",
                "DE",
                "DI",
                "CP",
                "LO",
            ]:
                return transaction_code
            else:
                print("Invalid transaction code.")


if __name__ == "__main__":
    app = BankingSystem()
    app.run()
