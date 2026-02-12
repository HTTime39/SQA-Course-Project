class TransactionFormatter:
  def format_deposit(self, account_holder_name, account_number, deposit_amount):
    record = f"04 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount(deposit_amount)}   \n" # There's two extra spaces at the end for the MM part of the formatting specification
    # print(record)
    return record
  
  def format_withdrawal(self, account_holder_name, account_number, withdrawal_amount):
    record = f"01 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount(withdrawal_amount)}   \n"
    return record
  
  # This will return two transaction records, the last two characters of the transaction record denote the sender as SS and the recipient by RR
  def format_transfer(self, account_holder_name, from_account_number, to_account_number, transfer_amount):
    record = f"02 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(from_account_number)} {self.format_deposit_amount(transfer_amount)} SS\n"
    record += f"02 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(to_account_number)} {self.format_deposit_amount(transfer_amount)} RR\n"
    # print(record)
    return record
  
  def format_pay_bill(self, account_holder_name, account_number, billing_company, pay_amount):
    record = f"03 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount(pay_amount)} {billing_company}\n" 
    return record
  
  def format_create_account(self, account_holder_name, account_number, initial_account_balance):
    record = f"05 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount(initial_account_balance)}   \n"
    return record
  
  def format_delete_account(self, account_holder_name, account_number):
    record = f"06 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount("")}   \n"
    return record
  
  def format_disable_account(self, account_holder_name, account_number):
    record = f"07 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount("")}   \n"
    return record
  
  def format_change_account_plan(self, account_holder_name, account_number, account_plan):
    record = f"08 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_deposit_amount("")} {account_plan}\n"
    return record
  
  def format_logout(self):
    record = f"00 {self.format_account_holder_name("")} {self.format_account_number("")} {self.format_deposit_amount("")}   \n"
    return record
  
  # Helper functions to match the formatting of the records
  def format_account_holder_name(self, account_holder_name):
    # Adding space to the name field to reach the fixed length requirement
    while (len(account_holder_name) < 20):
      account_holder_name += " "
    return account_holder_name
  
  def format_account_number(self, account_number):
    # Adding zeros to the account number to reach the fixed length requirement
    while (len(account_number) < 5):
      account_number = "0" + account_number
    return account_number
  
  def format_deposit_amount(self, deposit_amount):
    # Adding zeros to the deposit amount to reach the fixed length requirement
    while (len(deposit_amount) < 8): # TODO: This needs to append .00 etc. to the end of deposit amounts or the input must already be validated into this format; currently the validation in transaction_executor omits decimal numbers as '.' is non-numeric
      deposit_amount = "0" + deposit_amount
    return deposit_amount
  