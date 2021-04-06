import datetime
import random

# User database
database = {
    "seyi@bank.com": {
        "firstname" : "Seyi",
        "lastname"  : "Z",
        "accountNum": 132166548,
        "password"  : "passwordSeyi",
        "balance"   : 1200
        },
    "mike@bank.com": {
        "firstname" : "Mike",
        "lastname"  : "R",
        "accountNum": 465139548,
        "password"  : "passwordMike",
        "balance"   : 1300
        },
    "love@bank.com": {
        "firstname" : "Love",
        "lastname"  : "R",
        "accountNum": 654649116,
        "password"  : "passwordLove",
        "balance"   : 1400
        },
    }

# Current user logged in
CURRENT_USER = ""

# Welcome menu options
welcomeOptions = [
    [1, "Login"],
    [2, "Register"],
    [3, "Exit"],
    ]

# Banking menu options
bankOptions = [
    [1, "Withdrawal"],
    [2, "Cash Deposit"],
    [3, "Complaint"],
    [4, "View Account Info"],
    [5, "Change password"],
    [6, "Logout"],
    [7, "Logout and Exit"],
    ]

# Previous menu statements
returnMenu = "Returning to previous menu...\n"
prevMenu = "Enter \"Back\" to return to previous menu.\n"

# Invalid option statement
invalidOption = "Invalid option. Please try again.\n"


def welcome():
    """
    Displays the welcome menu for ATM users.
    """

    # Loop menu for invalid options
    while 1:

        # Print welcome message and menu options
        print("Welcome to the Improved ATM.\nPlease select an option:")
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
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    email = input("Enter your email: ").casefold()
    password = input("Create your password: ")

    # Generate account number
    account_number = generate_account_number()

    # Add new user to database
    database.update({email: {"firstname": firstname, "lastname": lastname, "accountNum": account_number,
                             "password" : password, "balance": 2000
                             }
                     })

    # Display registration results to user
    print("\nRegistration complete!\nPlease save your account number for your records:")
    display_account(email)


def generate_account_number():
    """
    Generate account number using random 9-digit number
    """
    return random.randrange(111111111, 999999999)


def login():
    """
    Log user in to account
    """

    # Ask user for email
    print("\n*** Existing user login ***\n" + prevMenu)
    user = input("Please enter your email: ").casefold()

    # Check if user wants to return to previous menu
    if user == "back":
        print(returnMenu)
        return

    # Ask for password
    password = input("Please enter your password: ")

    # Determine if email exists and validate password
    #  - if valid, go to banking menu
    #  - if invalid, retry login
    if user in database and database[user]["password"] == password:
        global CURRENT_USER
        CURRENT_USER = user
        bank_operations()
        return
    else:
        print("Incorrect email/password. Please try again.")
        login()


def bank_operations():
    """
    Displays bank operations menu.
    """

    # Get current time and display welcome message
    time = datetime.datetime.now()
    print("\nWelcome {0}!\nToday is {1}".format(database[CURRENT_USER]["firstname"], time.strftime("%A, %d %B %Y %X")))

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
            display_account(CURRENT_USER)
        elif select_option == 5:
            change_password()
        elif select_option == 6:
            logout()
            break
        elif select_option == 7:
            logout()
            quit_atm()
        else:
            print(invalidOption)


def withdraw():
    """
    Allows user to withdraw from available balance
    """

    # Display available balance and get withdrawal amount
    print("\nAvailable balance is: ${:.2f}.".format(database[CURRENT_USER]["balance"]))
    withdrawal_amount = input("Input the amount to withdraw.\n" + prevMenu + "$").casefold()

    # Validate withdrawal amount
    if withdrawal_amount.isnumeric():
        withdrawal_amount = int(withdrawal_amount)
        if withdrawal_amount > database[CURRENT_USER]["balance"]:
            print("\n" + "*" * 52)
            print("*** Cannot withdraw more than available balance! ***")
            print("*" * 52)
            withdraw()
        else:
            print("Retrieving ${:.2f}...\nPlease take your cash.\n".format(withdrawal_amount))
            database[CURRENT_USER]["balance"] = database[CURRENT_USER]["balance"] - withdrawal_amount
            print("Remaining balance is: ${:.2f}.\n".format(database[CURRENT_USER]["balance"]))
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
    print("\nCurrent balance is: ${:.2f}.".format(database[CURRENT_USER]["balance"]))
    deposit_amount = input("Input the amount to deposit.\n" + prevMenu + "$").casefold()

    # Validate deposit amount
    if deposit_amount.isnumeric():
        deposit_amount = int(deposit_amount)
        database[CURRENT_USER]["balance"] = database[CURRENT_USER]["balance"] + deposit_amount
        print("Depositing ${:.2f}...\nYour balance is now ${:.2f}\n"
              .format(deposit_amount, database[CURRENT_USER]['balance']))
    elif deposit_amount == "back":
        print(returnMenu)
        return
    else:
        print("Invalid input.")
        deposit()


def complaint():
    """
    Allows user to enter a complaint.
    """

    # Get user complaint
    complaint_entry = input("\nPlease enter your complaint.\n" + prevMenu).casefold()
    if complaint_entry == "back":
        print(returnMenu)
        return
    elif complaint_entry != "back":
        print("Thank you for letting us know.\n")


def display_account(user: str):
    """
    Displays account information.
    :param user: The user to display account info for
    """
    print("======================")
    print("Email: {}".format(user))
    for key, value in database[user].items():
        if key == "password":
            continue
        elif key == "balance":
            value = "${:.2f}".format(value)
        print("{0}: {1}".format(key.capitalize(), value))
    print("======================\n")


def change_password():
    """
    Allows user to change password.
    """
    print("\nChange user password.\n" + prevMenu)
    current_pw = input("Enter current password: ")
    if current_pw == "back":
        print(returnMenu)
        return
    new_pw1 = input("Enter new password: ")
    new_pw2 = input("Re-enter new password: ")

    if current_pw == database[CURRENT_USER]["password"] and new_pw1 == new_pw2:
        database[CURRENT_USER]["password"] = new_pw1
        print("\n*** Password for {} has been updated!\n".format(CURRENT_USER))
    else:
        print("\n*** Error: Either current password is incorrect,"
              "or new password entries did not match.\nPlease try again.\n")
        change_password()


def logout():
    """
    Log out user and return to welcome menu
    """
    global CURRENT_USER
    print("\n*** Logging out user {} ***\n".format(CURRENT_USER))
    CURRENT_USER = ""


def quit_atm():
    """
    Quit the program
    """
    print("Thank you for using Improved ATM. Have a good day.")
    quit()


# Display the welcome menu
welcome()
