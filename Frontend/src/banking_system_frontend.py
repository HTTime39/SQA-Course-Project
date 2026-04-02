"""
Banking System Frontend

This program allows users to log in as either a standard user (SU) or an admin user (AU)
and perform banking transactions through a menu. For each transaction, a formatted
transaction record is generated and stored.

Input files:
- current_bank_accounts.txt: Contains the list of existing bank accounts.

Output files:
- bank_account_transactions.txt: Contains the transaction records generated during a session.

Instructions:
1. Open the terminal
2. Change the directory to 'frontend/src': cd frontend/src
3. Run this file: python banking_system_frontend.py <current_bank_accounts_file> <bank_account_transactions_file>
"""

from session import Session
from bank_accounts import BankAccounts
from transaction_executor import TransactionExecutor
from transaction_file_writer import TransactionFileWriter
import sys


class BankingSystemFrontend:
    """
    Main class for the banking system front-end.
    Coordinates user login, menu display, transaction handling, and session termination.
    """

    def __init__(self, current_bank_accounts_file, bank_account_transactions_file):
        """
        Constructs a BankingSystemFrontend object.
        """
        self.session = None
        self.accounts = BankAccounts()
        self.executor = TransactionExecutor(self.accounts)
        self.writer = TransactionFileWriter(bank_account_transactions_file)
        self.current_bank_accounts_file = current_bank_accounts_file

    def run(self):
        """
        Runs the main program loop.
        """
        print("Banking System\n")
        self.login()
        self.accounts.load_accounts(self.current_bank_accounts_file)

        while self.session.is_active:
            if self.session.user_type == "SU":
                self.display_standard_menu()
            else:
                self.display_admin_menu()

        self.logout()

    def login(self):
        """
        Handles user login.
        Prompts the user to select a user type and initializes a Session object.
        """
        print("Login Menu\nStandard User: SU\nAdmin User: AU\n")
        user_type = self.prompt_user_type()

        if user_type == "SU":
            username = self.prompt_username()
            self.session = Session(user_type="SU", username=username, is_active=True)
        else:
            self.session = Session(user_type="AU", username="", is_active=True)

    def display_standard_menu(self):
        """
        Displays the standard user menu and processes the selected transaction.
        """
        print(
            "\nStandard User Menu\nDeposit: DP\nWithdrawal: WD\nTransfer: TR\nPay Bill: PB\nLogout: LO\n"
        )
        transaction_code = self.prompt_transaction_code()
        self.handle_transaction(transaction_code)

    def display_admin_menu(self):
        """
        Displays the admin user menu and processes the selected transaction.
        """
        print(
            "\nAdmin User Menu\nDeposit: DP\nWithdrawal: WD\nTransfer: TR\nPay Bill: PB\n"
            + "Create Account: CA\nDelete Account: DE\nDisable Account: DI\nChange Account Plan: CP\nLogout: LO\n"
        )
        transaction_code = self.prompt_transaction_code()
        self.handle_transaction(transaction_code)

    def handle_transaction(self, transaction_code):
        """
        Dispatches the transaction code to the corresponding handler method
        in TransactionExecutor and writes any generated transaction record
        to the output file.
        :param transaction_code: Selected transaction code
        """
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
        """
        Handles program logout.
        Generates and writes the logout transaction record.
        """
        transaction_record = self.executor.execute_logout()
        if transaction_record:
            self.writer.write_transaction_record(transaction_record)

        print("Logout completed.")

    def prompt_user_type(self):
        """
        Prompts the user to enter a user type.
        :return: Validated user type string
        """
        while True:
            user_type = input("Enter user type: ").strip().upper()
            if user_type in ["SU", "AU"]:
                return user_type
            else:
                print("Invalid user type.")

    def prompt_username(self):
        """
        Prompts the user to enter an account holder name for a standard user session.
        :return: Validated account holder name string
        """
        while True:
            username = input("Enter account holder name: ").strip().title()
            if 1 <= len(username) <= 20:
                return username
            else:
                print("Invalid username: Must be 1-20 characters.")

    def prompt_transaction_code(self):
        """
        Prompts the user to enter a transaction code from the displayed menu.
        :return: Validated transaction code string
        """
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
    if len(sys.argv) != 3:
        print(
            "Usage: python banking_system_frontend.py <current_bank_accounts_file> <bank_account_transactions_file>"
        )
        sys.exit(1)

    current_bank_accounts_file = sys.argv[1]
    bank_account_transactions_file = sys.argv[2]

    app = BankingSystemFrontend(
        current_bank_accounts_file, bank_account_transactions_file
    )
    app.run()
