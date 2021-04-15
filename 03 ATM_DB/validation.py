import re
import sys

import database_atm

# Error messages
error = "\n*** Error: "


def validate_account_num(acct_num: int) -> bool:
    """
    Verifies the account number does not already exist
    :param acct_num: account number to validate
    :return: True if account number is unique, otherwise False
    """
    # If account number exists, return False
    # Otherwise, it's unique, return True
    if database_atm.find("accountNum", acct_num):
        return False
    else:
        return True


def validate_email_format(email: str) -> bool:
    """
    Validate a simple email address
    :param email: the email to validate
    :return: True if valid, otherwise False
    """
    if re.search(r"\S+@\S+\.\S+", email):
        return True
    else:
        return False


def validate_email_in_use(email: str) -> bool:
    """
    Determines if provided email is already used for an account
    :param email: email to validate
    :return: True if email is in use, otherwise False
    """
    # If email exists, return False
    # Otherwise, it's unique, return True
    if database_atm.find("email", email):
        return True
    else:
        return False


def validate_login(email: str, password: str):
    """
    Validate login credentials
    :param email: email to login with
    :param password: password to validate
    :return: user dictionary if successful;
             "back" if there's a current session;
             otherwise False
    """

    # Get user information
    user_data = database_atm.find("email", email)

    # Verify user was found
    if not user_data:
        return False
    else:
        user_data = user_data[0]

    # Verify password
    if user_data["password"] == password:
        # Set auth_session file
        try:
            session_file = open(database_atm.auth_session_file, "x")
            session_file.write(user_data["email"])
            session_file.close()
            return user_data
        except FileExistsError:
            print(error + "Login session already exists. Logout/Exit to continue.\n")
            return "back"
        except IOError:
            sys.exit(error + "Cannot create login session. Please try again\n")
    else:
        return False
