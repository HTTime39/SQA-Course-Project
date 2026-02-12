class TransactionFormatter:
  # Prepares deposit transaction record
  def format_deposit(self, account_holder_name, account_number, deposit_amount):
    record = f"04 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount(deposit_amount)}   \n" # There's two extra spaces at the end for the MM part of the formatting specification
    # print(record)
    return record
  
  # Prepares withraw transaction record
  def format_withdrawal(self, account_holder_name, account_number, withdrawal_amount):
    record = f"01 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount(withdrawal_amount)}   \n"
    return record
  
  # Prepares format transaction record
  # This will return two transaction records, the last two characters of the transaction record denote the sender as SS and the recipient by RR
  def format_transfer(self, account_holder_name, from_account_number, to_account_number, transfer_amount):
    record = f"02 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(from_account_number)} {self.format_amount(transfer_amount)} SS\n"
    record += f"02 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(to_account_number)} {self.format_amount(transfer_amount)} RR\n"
    # print(record)
    return record
  
  # Prepares pay bill transaction record
  def format_pay_bill(self, account_holder_name, account_number, billing_company, pay_amount):
    record = f"03 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount(pay_amount)} {billing_company}\n" 
    return record
  
  # Prepares create account transaction record
  def format_create_account(self, account_holder_name, account_number, initial_account_balance):
    record = f"05 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount(initial_account_balance)}   \n"
    return record
  
  # Prepares delete account transaction record
  def format_delete_account(self, account_holder_name, account_number):
    record = f"06 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount("")}   \n"
    return record
  
  # Prepares disable account transaction record
  def format_disable_account(self, account_holder_name, account_number):
    record = f"07 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount("")}   \n"
    return record
  
  # Prepares change account plan transaction record
  def format_change_account_plan(self, account_holder_name, account_number, account_plan):
    record = f"08 {self.format_account_holder_name(account_holder_name)} {self.format_account_number(account_number)} {self.format_amount("")} {account_plan}\n"
    return record
  
  # Prepares logout transaction record
  def format_logout(self):
    record = f"00 {self.format_account_holder_name("")} {self.format_account_number("")} {self.format_amount("")}   \n"
    return record
  
  # Helper functions to match the formatting of the records
  # Adding space to the name field to reach the fixed length requirement
  def format_account_holder_name(self, account_holder_name):
    while (len(account_holder_name) < 20):
      account_holder_name += " "
    return account_holder_name
  
  # Adding zeros to the account number to reach the fixed length requirement
  def format_account_number(self, account_number):
    while (len(account_number) < 5):
      account_number = "0" + account_number
    return account_number
  
  # Adding zeros to the deposit amount to reach the fixed length requirement
  def format_amount(self, amount):
    while (len(amount) < 8): # TODO: This needs to append .00 etc. to the end of deposit amounts or the input must already be validated into this format; currently the validation in transaction_executor omits decimal numbers as '.' is non-numeric
      amount = "0" + amount
    return amount
  