from decimal import Decimal, InvalidOperation


class AccountRecordBuilder:
    """
    Builds account records.
    """

    def build_account_record(self, file_type, account_number, account_data):
        """
        Builds an account record.
        :param file_type: Output file type
        :param account_number: Account number
        :param account_data: Account data
        :return: Account record
        """
        account_holder_name = self.format_account_holder_name(account_data)
        account_balance = self.format_account_balance(account_data)
        account_status = account_data["status"]

        if file_type == "new_master_bank_accounts_file":
            num_transactions = self.format_num_transactions(account_data)
            return f"{account_number} {account_holder_name} {account_status} {account_balance} {num_transactions}"
        elif file_type == "current_bank_accounts_file":
            return f"{account_number} {account_holder_name} {account_status} {account_balance}"
        else:
            raise ValueError("Invalid file type")

    def format_account_holder_name(self, account_data):
        """
        Formats an account holder name to 20 characters.
        :param account_data: Account data
        :return: Formatted account holder name
        """
        account_holder_name = account_data["holder_name"]
        return account_holder_name.ljust(20)[:20]

    def format_account_balance(self, account_data):
        """
        Formats an account balance to 8 characters.
        :param account_data: Account data
        :return: Formatted account balance
        """
        account_balance = account_data["balance"]

        try:
            value = Decimal(account_balance)
        except (InvalidOperation, TypeError):
            value = Decimal("0.00")

        return f"{value:08.2f}"

    def format_num_transactions(self, account_data):
        """
        Formats a transaction count to 4 characters.
        :param account_data: Account data
        :return: Formatted transaction count
        """
        num_transactions = int(account_data["num_transactions"])
        return str(num_transactions).zfill(4)
