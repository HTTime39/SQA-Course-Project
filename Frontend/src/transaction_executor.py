from transaction_formatter import TransactionFormatter
from decimal import Decimal, InvalidOperation


class TransactionExecutor:
    """
    Executes user-requested banking transactions and coordinates
    user input and transaction formatting.
    """

    def __init__(self, accounts):
        """
        Constructs a TransactionExecutor object.
        :param accounts: BankAccounts object
        """
        self.formatter = TransactionFormatter()
        self.accounts = accounts
        self.account_number = None

    def execute_deposit(self, session):
        """
        Executes a deposit transaction.
        :param session: Session object
        :return: Formatted transaction record string
        """
        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name, session
        )
        deposit_amount = self.prompt_amount("Enter amount to deposit: $", "DP", session)

        return self.formatter.format_deposit(
            account_holder_name, account_number, deposit_amount
        )

    def execute_withdrawal(self, session):
        """
        Executes a withdrawal transaction.
        :param session: Session object
        :return: Formatted transaction record string
        """
        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name, session
        )
        withdrawal_amount = self.prompt_amount(
            "Enter amount to withdraw: $", "WD", session
        )

        return self.formatter.format_withdrawal(
            account_holder_name, account_number, withdrawal_amount
        )

    def execute_transfer(self, session):
        """
        Executes a transfer transaction.
        :param session: Session object
        :return: Formatted transaction record string
        """
        account_holder_name = self.get_account_holder_name(session)
        from_account_number = self.prompt_account_number(
            "Enter account number of account to transfer from: ", account_holder_name, session
        )
        while (True): # Looping until a to account is chosen that is not the same as the from account
          to_account_number = self.prompt_account_number(
            "Enter account number of account to transfer to: ", account_holder_name, session
          )
          if to_account_number == from_account_number:
            print("Invalid transfer: Account numbers are the same.")
          else:
            break

        transfer_amount = self.prompt_amount(
            "Enter amount to transfer: $", "TR", session
        )

        return self.formatter.format_transfer(
            account_holder_name, from_account_number, to_account_number, transfer_amount
        )

    def execute_pay_bill(self, session):
        """
        Executes a pay bill transaction.
        :param session: Session object
        :return: Formatted transaction record string
        """
        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name, session
        )
        billing_company = self.prompt_billing_company()
        pay_amount = self.prompt_amount("Enter amount to pay: $", "PB", session)

        return self.formatter.format_pay_bill(
            account_holder_name, account_number, billing_company, pay_amount
        )

    def execute_create_account(self, session):
        """
        Executes a create account transaction.
        :param session: Session object
        :return: Formatted transaction record string or None for standard users
        """
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.prompt_account_holder_name()
        account_number = self.generate_account_number()
        self.display_account_plan_menu()
        account_plan = self.prompt_account_plan()

        return self.formatter.format_create_account(
            account_holder_name, account_number, account_plan
        )

    def execute_delete_account(self, session):
        """
        Executes a delete account transaction.
        :param session: Session object
        :return: Formatted transaction record string or None for standard users
        """
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name, session
        )

        return self.formatter.format_delete_account(account_holder_name, account_number)

    def execute_disable_account(self, session):
        """
        Executes a disable account transaction.
        :param session: Session object
        :return: Formatted transaction record string or None for standard users
        """
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name, session
        )

        return self.formatter.format_disable_account(
            account_holder_name, account_number
        )

    def execute_change_account_plan(self, session):
        """
        Executes a change account plan transaction.
        :param session: Session object
        :return: Formatted transaction record string or None for standard users
        """
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name, session
        )
        self.display_account_plan_menu()
        account_plan = self.prompt_account_plan()

        return self.formatter.format_change_account_plan(
            account_holder_name, account_number, account_plan
        )

    def prompt_account_holder_name(self):
        """
        Prompts the user to enter an account holder name.
        :return: Validated account holder name string
        """
        while True:
            account_holder_name = input("Enter account holder name: ").strip().title()
            if 1 <= len(account_holder_name) <= 20:
                return account_holder_name
            else:
                print("Invalid account holder name: Must be 1-20 characters.")

    def prompt_account_number(self, prompt, account_holder_name, session=None):
        """
        Prompts the user to enter an account number.
        :param prompt: Prompt message
        :param account_holder_name: Account holder name
        :param session: Session object (optional). Used to format admin vs standard error messages.
        :return: Validated account number string
        """
        is_admin = session is not None and getattr(session, "user_type", None) == "AU"

        while True:
            account_number = input(prompt).strip()
            if not account_number.isdigit():
                # Keep the original wording for both user types (matches provided expected outputs)
                print("Invalid account number: Must be numeric.")
                continue
            elif not self.accounts.account_exists(account_holder_name, account_number):
                # Expected admin wording differs from standard wording
                if is_admin:
                    print("Invalid: Account does not exist.")
                else:
                    print("Invalid account: Does not exist.")
                continue
            elif not self.accounts.is_account_active(account_number):
                if is_admin:
                    print("Invalid: Account is disabled.")
                else:
                    print("Invalid account: Disabled.")
                continue

            self.account_number = account_number
            return account_number

    def prompt_billing_company(self):
        """
        Prompts the user to enter a billing company code.
        :return: Validated billing company code string
        """
        while True:
            billing_company = input("Enter billing company code: ").strip().upper()
            if billing_company.isalnum() and len(billing_company) == 2:
                return billing_company
            else:
                print("Invalid billing company code: Must be 2 characters.")

    def prompt_account_plan(self):
        """
        Prompts the user to select an account plan.
        :return: Selected account plan string
        """
        while True:
            selection = input("Enter account plan selection: ").strip()
            if selection == "1":
                return "SP"
            elif selection == "2":
                return "NP"
            else:
                print("Invalid selection: Must be 1 or 2.")

    def prompt_amount(self, prompt, transaction_code, session):
        """
        Prompts the user to enter a monetary amount.
        :param prompt: Prompt message
        :param transaction_code: Transaction code (e.g., DP, WD, TR, PB)
        :param session: Session object
        :return: Formatted amount string
        """
        while True:
            amount = input(prompt).strip()

            try:
                value = Decimal(amount)
            except InvalidOperation:
                print("Invalid amount: Must be numeric.")
                continue

            if value < Decimal("0.00"):
                print("Invalid amount: Cannot be negative.")
                continue

            # Session maximum checks for Standard Users
            if session.user_type == "SU":
                if transaction_code == "WD" and value > Decimal("500.00"):
                    print("Invalid amount: Session maximum is $500.")
                    continue
                if transaction_code == "TR" and value > Decimal("1000.00"):
                    print("Invalid amount: Session maximum is $1000.")
                    continue
                if transaction_code == "PB" and value > Decimal("2000.00"):
                    print("Invalid amount: Session maximum is $2000.")
                    continue

            # Prevent transactions that would result in a negative balance
            if transaction_code in {"WD", "TR", "PB"}:
                account_balance = Decimal(
                    self.accounts.get_account_balance(self.account_number)
                )
                if account_balance - value < Decimal("0.00"):
                    print("Invalid amount: Cannot result in a negative balance.")
                    continue

            return f"{value:.2f}"

    def display_account_plan_menu(self):
        """
        Displays the account plan selection menu.
        """
        print("Select account plan:")
        print("1. Student Plan (SP)")
        print("2. Non-Student Plan (NP)")

    def generate_account_number(self):
        """
        Generates a unique account number not currently in use.
        :return: Account number string
        """
        while True:
            account_number = str(random.randint(10000, 99999))
            if not self.accounts.account_number_in_use(account_number):
                return account_number

    def get_account_holder_name(self, session):
        """
        Determines the account holder name based on the user type.
        :param session: Session object
        :return: Account holder name string
        """
        if session.user_type == "AU":
            account_holder_name = self.prompt_account_holder_name()
        else:
            account_holder_name = session.username

        return account_holder_name