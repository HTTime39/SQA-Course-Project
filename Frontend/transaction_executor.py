from transaction_formatter import TransactionFormatter


class TransactionExecutor:
    def __init__(self, accounts):
        self.formatter = TransactionFormatter()
        self.accounts = accounts

    def execute_deposit(self, session):
        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name
        )
        deposit_amount = self.prompt_amount("Enter amount to deposit: $")

        return self.formatter.format_deposit(
            account_holder_name, account_number, deposit_amount
        )

    def execute_withdrawal(self, session):
        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name
        )
        withdrawal_amount = self.prompt_amount("Enter amount to withdrawal: $")

        return self.formatter.format_withdrawal(
            account_holder_name, account_number, withdrawal_amount
        )

    def execute_transfer(self, session):
        account_holder_name = self.get_account_holder_name(session)
        from_account_number = self.prompt_account_number(
            "Enter account number of account to transfer from: ", account_holder_name
        )
        to_account_number = self.prompt_account_number(
            "Enter account number of account to transfer to: ", account_holder_name
        )
        transfer_amount = self.prompt_amount("Enter amount to transfer: $")

        return self.formatter.format_transfer(
            account_holder_name, from_account_number, to_account_number, transfer_amount
        )

    def execute_pay_bill(self, session):
        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name
        )
        billing_company = self.prompt_billing_company()
        pay_amount = self.prompt_amount("Enter amount to pay: $")

        return self.formatter.format_pay_bill(
            account_holder_name, account_number, billing_company, pay_amount
        )

    def execute_create_account(self, session):
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.accounts.generate_account_number()
        initial_account_balance = self.prompt_amount("Enter initial account balance: $")

        return self.formatter.format_create_account(
            account_holder_name, account_number, initial_account_balance
        )

    def execute_delete_account(self, session):
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name
        )

        return self.formatter.format_delete_account(account_holder_name, account_number)

    def execute_disable_account(self, session):
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name
        )

        return self.formatter.format_disable_account(
            account_holder_name, account_number
        )

    def execute_change_account_plan(self, session):
        if session.user_type != "AU":
            print("Invalid transaction: Privileged.")
            return None

        account_holder_name = self.get_account_holder_name(session)
        account_number = self.prompt_account_number(
            "Enter account number: ", account_holder_name
        )
        self.display_account_plan_menu()
        account_plan = self.prompt_account_plan()

        return self.formatter.format_change_account_plan(
            account_holder_name, account_number, account_plan
        )

    def execute_logout(self):
        return self.formatter.format_logout()

    def get_account_holder_name(self, session):
        if session.user_type == "AU":
            account_holder_name = self.prompt_account_holder_name()
        else:
            account_holder_name = session.username

        return account_holder_name

    def prompt_account_holder_name(self):
        while True:
            account_holder_name = input("Enter account holder name: ").strip().title()
            if 1 <= len(account_holder_name) <= 20:
                return account_holder_name
            else:
                print("Invalid account holder name: Must be 1-20 characters.")

    def prompt_account_number(self, prompt, account_holder_name):
        while True:
            account_number = input(prompt).strip()
            if not account_number.isdigit():
                print("Invalid account number: Must be numeric.")
                continue

            if not self.accounts.account_exists(account_holder_name, account_number):
                print("Invalid account: Does not exist.")
                continue

            if not self.accounts.is_account_active(account_number):
                print("Invalid account: Disabled.")
                continue

            return account_number

    def prompt_amount(self, prompt):
        while True:
            amount = input(prompt).strip()
            try:
                value = float(amount)
                if value > 0:
                    return f"{value:.2f}"
            except ValueError:
                pass
            print("Invalid amount.")

    def prompt_billing_company(self):
        self.display_billing_company_menu()
        while True:
            billing_company = input("Enter billing company code: ").strip().upper()

            if billing_company in ["EC", "CQ", "FI"]:
                return billing_company
            else:
                print("Invalid company code.")

    def prompt_account_plan(self):
        while True:
            account_plan = input("Enter account plan: ").strip().upper()
            if account_plan in ["SP", "NP"]:
                return account_plan
            else:
                print("Invalid account plan.")

    def display_billing_company_menu(self):
        print(
            "\nCompany Menu\nThe Bright Light Electric Company: EC\nCredit Card Company Q: CQ\nFast Internet, Inc.: FI\n"
        )

    def display_account_plan_menu(self):
        print("\nAccount Plan Menu\nStudent Plan: SP\nNon-student Plan: NP")
