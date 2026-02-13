class TransactionFormatter:
    def __init__(self):
        pass

    # Prepares deposit transaction record
    def format_deposit(self, account_holder_name, account_number, deposit_amount):
        transaction_code = "04"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, deposit_amount, ""
        )

    # Prepares withdrawal transaction record
    def format_withdrawal(self, account_holder_name, account_number, withdrawal_amount):
        transaction_code = "01"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, withdrawal_amount, ""
        )

    # Prepares format transaction record
    def format_transfer(
        self,
        account_holder_name,
        from_account_number,
        to_account_number,
        transfer_amount,
    ):
        transaction_code = "02"
        miscellaneous_data = self.format_account_number(to_account_number)
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            from_account_number,
            transfer_amount,
            miscellaneous_data,
        )

    # Prepares pay bill transaction record
    def format_pay_bill(
        self, account_holder_name, account_number, billing_company, pay_amount
    ):
        transaction_code = "03"
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            account_number,
            pay_amount,
            billing_company,
        )

    # Prepares create account transaction record
    def format_create_account(
        self, account_holder_name, account_number, initial_account_balance
    ):
        transaction_code = "05"
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            account_number,
            initial_account_balance,
            "",
        )

    # Prepares delete account transaction record
    def format_delete_account(self, account_holder_name, account_number):
        transaction_code = "06"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, "0", ""
        )

    # Prepares disable account transaction record
    def format_disable_account(self, account_holder_name, account_number):
        transaction_code = "07"
        return self.build_transaction_record(
            transaction_code, account_holder_name, account_number, "0", "D"
        )

    # Prepares change account plan transaction record
    def format_change_account_plan(
        self, account_holder_name, account_number, account_plan
    ):
        transaction_code = "08"
        return self.build_transaction_record(
            transaction_code,
            account_holder_name,
            account_number,
            "0",
            account_plan,
        )

    # Prepares logout transaction record
    def format_logout(self):
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

    # Helper functions to match the formatting of the records
    # Adding spaces to the name field to reach the fixed length requirement
    def format_account_holder_name(self, account_holder_name):
        account_holder_name = account_holder_name.strip().title().replace(" ", "_")
        while len(account_holder_name) < 20:
            account_holder_name += "_"
        return account_holder_name

    # Adding zeros to the account number to reach the fixed length requirement
    def format_account_number(self, account_number):
        while len(account_number) < 5:
            account_number = "0" + account_number
        return account_number

    # Adding zeros to the amount to reach the fixed length requirement
    def format_amount(self, amount):
        try:
            value = float(amount)
        except ValueError:
            value = 0.0
        return f"{value:08.2f}"

    def format_miscellaneous_data(self, miscellaneous_data):
        return miscellaneous_data.ljust(2, "_")[:2]
