class AccountRecordBuilder:
    """
    Formats account information according to the required fixed-width record format. It ensures that account numbers, names, balances, and transaction counts follow the correct formatting specification.
    """
    def build_account_record(self, account_number, account_holder_name, account_status, account_balance, num_transactions):
        """
        Builds a formatted account record according to the required fixed-width output format.
        """
        return f"${account_number} ${self.format_account_holder_name(account_holder_name)} ${account_status} ${self.format_account_balance(account_balance)} ${self.format_num_transactions(num_transactions)}"

    def format_account_holder_name(self, account_data):
        """
        Formats the account holder name to a fixed width of twenty characters by padding with spaces if necessary.
        """
        while (len(account_data) < 20):
            account_data += " "
        return account_data

    def format_account_balance(self, account_data):
        """
        Formats the account balance to an eight-character monetary value.
        """
        while (len(account_data) < 8):
            account_data = "0" + account_data
        return account_data

    def format_num_transactions(self, account_data):
        """
        Formats the number of transactions as a four-digit value.
        """
        while (len(account_data) < 4):
            account_data = "0" + account_data
        return account_data
