class TransactionFormatter:
    """
    Formats banking transactions into fixed-length transaction record strings.
    """

    def format_deposit(self, account_holder_name, account_number, deposit_amount):
        """
        Formats a deposit transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param deposit_amount: Deposit amount
        :return: Formatted transaction record string
        """
        transaction_code = "04"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, deposit_amount, ""
        )

    def format_withdrawal(self, account_holder_name, account_number, withdrawal_amount):
        """
        Formats a withdrawal transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param withdrawal_amount: Withdrawal amount
        :return: Formatted transaction record string
        """
        transaction_code = "01"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, withdrawal_amount, ""
        )

    def format_transfer(
        self,
        account_holder_name,
        from_account_number,
        to_account_number,
        transfer_amount,
    ):
        """
        Formats a transfer transaction record.
        :param account_holder_name: Account holder name
        :param from_account_number: Source account number
        :param to_account_number: Destination account number
        :param transfer_amount: Transfer amount
        :return: Formatted transaction record string
        """
        transaction_code = "02"
        miscellaneous_data = self.format_account_number(to_account_number)
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            from_account_number,
            transfer_amount,
            miscellaneous_data,
        )

    def format_pay_bill(
        self, account_holder_name, account_number, billing_company, pay_amount
    ):
        """
        Formats a pay bill transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param billing_company: Billing company code
        :param pay_amount: Payment amount
        :return: Formatted transaction record string
        """
        transaction_code = "03"
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            account_number,
            pay_amount,
            billing_company,
        )

    def format_create_account(
        self, account_holder_name, account_number, initial_account_balance
    ):
        """
        Formats a create account transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param initial_account_balance: Initial account balance
        :return: Formatted transaction record string
        """
        transaction_code = "05"
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            account_number,
            initial_account_balance,
            "",
        )

    def format_delete_account(self, account_holder_name, account_number):
        """
        Formats a delete account transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :return: Formatted transaction record string
        """
        transaction_code = "06"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, "0", ""
        )

    def format_disable_account(self, account_holder_name, account_number):
        """
        Formats a disable account transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :return: Formatted transaction record string
        """
        transaction_code = "07"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, "0", "D"
        )

    def format_change_account_plan(
        self, account_holder_name, account_number, account_plan
    ):
        """
        Formats a change account plan transaction record.
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param account_plan: Account plan code
        :return: Formatted transaction record string
        """
        transaction_code = "08"
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            account_number,
            "0",
            account_plan,
        )

    def format_logout(self):
        """
        Formats a logout transaction record.
        :return: Formatted transaction record string
        """
        transaction_code = "00"
        return transaction_code + ("_" * 22) + "00000_00000.00_00"

    def build_transaction_record(
        self,
        transaction_code,
        account_holder_name,
        account_number,
        amount,
        miscellaneous_data,
    ):
        """
        Builds a formatted transaction record string using fixed-length fields.
        :param transaction_code: Transaction code
        :param account_holder_name: Account holder name
        :param account_number: Account number
        :param amount: Transaction amount
        :param miscellaneous_data: Miscellaneous data field
        :return: Formatted transaction record string
        """
        account_holder_name_field = self.format_account_holder_name(account_holder_name)
        account_number_field = self.format_account_number(account_number)
        amount_field = self.format_amount(amount)

        if miscellaneous_data == "":
            miscellaneous_field = "__"
        else:
            miscellaneous_field = self.format_miscellaneous_data(miscellaneous_data)

        transaction_record = (
            transaction_code
            + "_"
            + account_holder_name_field
            + "_"
            + account_number_field
            + "_"
            + amount_field
            + "_"
            + miscellaneous_field
        )

        return transaction_record

    def format_account_holder_name(self, account_holder_name):
        """
        Formats the account holder name to a fixed-length field.
        :param account_holder_name: Account holder name
        :return: Formatted account holder name string
        """
        account_holder_name = account_holder_name.strip().title().replace(" ", "_")
        while len(account_holder_name) < 20:
            account_holder_name += "_"
        return account_holder_name

    def format_account_number(self, account_number):
        """
        Formats the account number to a fixed-length field.
        :param account_number: Account number
        :return: Formatted account number string
        """
        while len(account_number) < 5:
            account_number = "0" + account_number
        return account_number

    def format_amount(self, amount):
        """
        Formats a monetary amount to a fixed-length field.
        :param amount: Monetary amount
        :return: Formatted amount string
        """
        try:
            value = float(amount)
        except ValueError:
            value = 0.0
        return f"{value:08.2f}"

    def format_miscellaneous_data(self, miscellaneous_data):
        """
        Formats the miscellaneous data field to a fixed-length field.
        :param miscellaneous_data: Miscellaneous data value
        :return: Formatted miscellaneous data string
        """
        return miscellaneous_data.ljust(2, "_")[:2]
