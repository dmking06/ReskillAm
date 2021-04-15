import datetime
import random
from getpass import getpass

import sys

import database_atm
import validation

# Current user logged in
CURRENT_USER = {}

# Welcome menu options
welcomeOptions = [
    [1, "Login"],
    [2, "Register"],
    [3, "Exit"],
    ]

# Banking menu options
bankOptions = [
    [1, "Make a Withdrawal"],
    [2, "Make a Deposit"],
    [3, "File a Complaint"],
    [4, "View Account Info"],
    [5, "Change Password"],
    [6, "Close Account"],
    [7, "Logout"],
    [8, "Logout and Exit"],
    ]

# Try again statement
please_try = "Please try again."

# Previous menu statements
returnMenu = "Returning to previous menu...\n"
prevMenu = "Enter \"Back\" to return to previous menu.\n"

# Error statements
invalidOption = "Invalid option. " + please_try
error = "*** Error: "
transaction_error = error + "Could not complete transaction. " + please_try

# Separators
short_sep = "=" * 30
long_sep = "=" * 40
star_sep = "*" * 52


def welcome():
    """
    Displays the welcome menu for ATM users.
    """
    # Clear any open sessions
    database_atm.end_session()

    # Loop menu for invalid options
    while 1:

        # Print welcome message and menu options
        print("Welcome to the Database ATM.\nPlease select an option:")
        for option in welcomeOptions:
            print("{}: {}".format(option[0], option[1]))

        # Get user selection
        select_option = input()

        # Validate user selection is numeric
        if select_option.isnumeric():
            select_option = int(select_option)
        else:
            print(invalidOption)
            continue

        # Choose action based on user selection
        if select_option == 1:
            login()
        elif select_option == 2:
            register()
        elif select_option == 3:
            quit_atm()
        else:
            print(invalidOption)


def register():
    """
    Registers new users.
    """
    # Get user information
    print("\n*** New account registration ***")

    # Loop for valid email input
    while 1:
        print(prevMenu)
        # Ask user for email
        email = input("Enter your email: ").casefold()

        # Check if user wants to return to previous menu
        if email == "back":
            print(returnMenu)
            return

        # Validate email
        if not validation.validate_email_format(email):
            print(error + "Invalid email format. " + please_try)
        elif validation.validate_email_in_use(email):
            print(error + "Email is already associated with an account. " + please_try)
        else:
            break

    # Get firstname, lastname, and password
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    password = getpass("Create your password (case-sensitive): ")

    # Generate account number
    account_number = generate_account_number()

    # Add new user to database
    if database_atm.create(email=email, firstname=firstname, lastname=lastname,
                           acct_num=account_number, password=password, balance=0):
        # Display registration results to user
        print("\nRegistration complete!\nPlease save your account number for your records:")
        display_account(email)
    else:
        print(error + "Cannot create new user. " + please_try)


def generate_account_number() -> int:
    """
    Generate account number using random 10-digit number
    :return: a unique 10-digit account number
    """
    while 1:
        new_account = random.randrange(1111111111, 9999999999)

        # Verify the account number is unique
        if validation.validate_account_num(new_account):
            return new_account


def login():
    """
    Log user in to account
    """
    # Get a valid email
    email = ""
    valid_email = False
    while not valid_email:
        # Ask user for email
        print("\n*** Existing user login ***\n" + prevMenu)
        email = input("Please enter your email: ").casefold()

        # Check if user wants to return to previous menu
        if email == "back":
            print(returnMenu)
            return

        # Validate email
        valid_email = validation.validate_email_format(email)

    # Ask for password
    password = getpass("Please enter your password: ")

    # Validate
    #  - if valid, go to banking menu
    #  - if invalid, retry login
    valid_login = validation.validate_login(email, password)
    if type(valid_login) is dict:
        global CURRENT_USER
        CURRENT_USER = valid_login
        bank_operations()
    elif valid_login == "back":
        return
    else:
        print(error + "Incorrect email/password. " + please_try)
        login()


def bank_operations():
    """
    Displays bank operations menu.
    """
    # Get current time and display welcome message
    time = datetime.datetime.now()
    print("\n{}\nWelcome {}!\nToday is {}\n{}".
          format(long_sep, CURRENT_USER["firstname"], time.strftime("%A, %d %B %Y %X"), long_sep))

    # Loop menu for invalid selections
    while 1:
        # Display menu
        print("Banking options:")
        for option in bankOptions:
            print("{}. {}".format(option[0], option[1]))

        # Get user selection
        select_option = input("\nPlease select an option: ")

        # Validate user selection is numeric
        if select_option.isnumeric():
            select_option = int(select_option)
        else:
            print(invalidOption)
            continue

        # Choose action based on user selection
        if select_option == 1:
            withdraw()
        elif select_option == 2:
            deposit()
        elif select_option == 3:
            complaint()
        elif select_option == 4:
            display_account(CURRENT_USER["email"])
        elif select_option == 5:
            change_password()
        elif select_option == 6:
            if close_account():
                break
        elif select_option == 7:
            logout()
            break
        elif select_option == 8:
            logout()
            quit_atm()
        else:
            print(invalidOption)


def withdraw():
    """
    Allows user to withdraw from available balance
    """
    # Display available balance and get withdrawal amount
    print("\nAvailable balance is: ${:.2f}.".format(int(CURRENT_USER["balance"])))
    withdrawal_amount = input("Input the whole dollar amount to withdraw.\n" + prevMenu + "$").casefold()

    # Validate withdrawal amount
    if withdrawal_amount.isnumeric():
        withdrawal_amount = int(withdrawal_amount)
        if withdrawal_amount > CURRENT_USER["balance"]:
            print("\n" + star_sep)
            print("*** Cannot withdraw more than available balance! ***")
            print(star_sep)
            withdraw()
        else:
            CURRENT_USER["balance"] = CURRENT_USER["balance"] - withdrawal_amount
            if database_atm.update(CURRENT_USER):
                print("Retrieving ${:.2f}...\nPlease take your cash.\n".format(withdrawal_amount))
                print("Remaining balance is: ${:.2f}.\n".format(int(CURRENT_USER["balance"])))
            else:
                print(transaction_error)
                CURRENT_USER["balance"] = CURRENT_USER["balance"] + withdrawal_amount
                return
    elif withdrawal_amount == "back":
        print(returnMenu)
        return
    else:
        print("Invalid input.")
        withdraw()


def deposit():
    """
    Allows user to make a deposit.
    """
    # Display current balance and get deposit amount
    print("\nCurrent balance is: ${:.2f}.".format(CURRENT_USER["balance"]))
    deposit_amount = input("Input the whole dollar amount to deposit.\n" + prevMenu + "$").casefold()

    # Validate deposit amount
    if deposit_amount.isnumeric():
        deposit_amount = int(deposit_amount)
        CURRENT_USER["balance"] = CURRENT_USER["balance"] + deposit_amount
        if database_atm.update(CURRENT_USER):
            print("Depositing ${:.2f}...\nYour balance is now ${:.2f}\n"
                  .format(deposit_amount, CURRENT_USER['balance']))
        else:
            print(transaction_error)
            CURRENT_USER["balance"] = CURRENT_USER["balance"] - deposit_amount
    elif deposit_amount == "back":
        print(returnMenu)
    else:
        print("Invalid input.")
        deposit()


def complaint():
    """
    Allows user to enter a complaint.
    """
    # Get user complaint
    complaint_entry = input("\nPlease enter your complaint.\n" + prevMenu)
    if complaint_entry.casefold() == "back":
        print(returnMenu)
        return

    now = datetime.datetime.now()
    now = now.strftime("%c")
    if database_atm.file_complaint(CURRENT_USER["email"], complaint_entry, now):
        print("Thank you for letting us know.\n")
    else:
        print(please_try)


def display_account(user: str):
    """
    Displays account information.
    """
    print("\n{}".format(short_sep))
    acct_details = list(database_atm.find("email", user))[0]
    for key, value in acct_details.items():
        if key == "password":
            continue
        elif key == "balance":
            value = "${:.2f}".format(value)
        elif key == "email":
            value = "\t" + value
        print("{0}:\t{1}".format(key.capitalize(), value))
    print("{}\n".format(short_sep))


def change_password():
    """
    Allows user to change password.
    """
    # Get current password
    print("\nChange user password.\n" + prevMenu)
    current_pw = getpass("Enter current password: ")
    if current_pw == "back":
        print(returnMenu)
        return

    # Get new password
    new_pw1 = getpass("Enter new password: ")
    new_pw2 = getpass("Re-enter new password: ")

    # Validate old and new passwords
    if current_pw != CURRENT_USER["password"]:
        print(error + "Current password is incorrect. " + please_try)
        change_password()
    elif new_pw1 != new_pw2:
        print(error + "New password entries do not match. " + please_try)
        change_password()
    elif current_pw == new_pw1:
        print(error + "New password cannot be current password. " + please_try)
        change_password()
    else:
        # Change password
        CURRENT_USER["password"] = new_pw1
        if database_atm.update(CURRENT_USER):
            print("\n*** Password for {} has been updated!\n".format(CURRENT_USER["email"]))
        else:
            print(error + "Cannot update password. " + please_try)
            CURRENT_USER["password"] = current_pw


def close_account() -> bool:
    """
    Closes (deletes) the user account
    :return: True if successful, otherwise False
    """
    print(star_sep)
    print("Warning: You are about to close your account. Any\n"
          "remaining balance in your account will be issued as\n"
          "a cashier's check. Verify the account details below.")
    display_account(CURRENT_USER["email"])
    print(star_sep + "\n")

    print("*** To close your account, enter in your password.\n" + prevMenu)
    password = getpass("Enter password to close account: ")

    if password == "back":
        print(returnMenu)
        return False
    elif password == CURRENT_USER["password"]:
        if database_atm.delete(CURRENT_USER["email"]):
            print("*** Account for {} has been closed. Thank you for being a customer."
                  .format(CURRENT_USER["email"]))
            logout()
            return True
        else:
            print(error + "Could not close account. " + please_try)
            close_account()
            return False
    else:
        print(error + "Incorrect password. " + please_try)
        close_account()


def logout():
    """
    Log out user and return to welcome menu
    """
    global CURRENT_USER
    print("\n*** Logging out user {} ***\n".format(CURRENT_USER["email"]))
    CURRENT_USER.clear()
    database_atm.end_session()


def quit_atm():
    """
    Quit the program
    """
    if CURRENT_USER:
        database_atm.end_session()
    sys.exit("Thank you for using DB ATM. Have a good day.")


# Display the welcome menu
welcome()
