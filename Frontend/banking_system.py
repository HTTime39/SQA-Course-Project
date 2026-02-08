import re

from bank_accounts import Bank_Accounts
from session import Session
from transaction_executor import Transaction_Executor
from transaction_file_writer import Transaction_File_Writer
from transaction_formatter import Transaction_Formatter

class Banking_System:
  current_session = None
  logout_flag = False

  def main(self):
    print("Welcome to the Banking System")
    self.run()

    return
  
  def run(self):
    if (self.current_session == None):
      self.login()

    while (not self.logout_flag):
      selected_transaction = 0

      if (self.current_session.is_admin):
        selected_transaction = self.display_admin_menu()
      else:
        selected_transaction = self.display_standard_menu()

      # TODO: Implement calls to action execution. Use switch case?

    return
  
  def login(self):
    username = input("Please enter your username")
    password = input("Please enter your password")

    # TODO: Implement account information retrieval + validation

    return
  
  def display_standard_menu(self):
    valid_action = False
    selected_transaction = 0

    print("\nEnter a number to select an action:")
    
    while (not valid_action):
      selected_transaction = input("""
        1. Deposit 
        2. Withdraw 
        3. Transfer 
        4. Pay Bill
        5. Logout \n
      """)

      if (re.match(r"[12345]", selected_transaction)):
        valid_action = True
      else:
        print("\nInvalid selection. Enter a valid number to select an action:")

    return selected_transaction 
  
  def display_admin_menu(self):
    valid_action = False
    selected_transaction = 0

    print("\nEnter a number to select an action:")

    while (not valid_action):
      selected_transaction = input("""
        1. Deposit 
        2. Withdraw 
        3. Transfer 
        4. Pay Bill 
        5. Create Account 
        6. Delete Account 
        7. Disable Account 
        8. Change Account Plan 
        9. Logout \n
      """)

      if (re.match(r"[123456789]", selected_transaction)):
          valid_action = True
      else:
        print("\nInvalid selection. Enter a valid number to select an action:")

    return selected_transaction
  
  def hand_transaction(self, transaction_code):
    # TODO

    return
  
  def logout(self):
    self.logout_flag
    # TODO: Implement and call logout transaction execution
    return
  
# x = Banking_System()
# x.display_admin_menu()