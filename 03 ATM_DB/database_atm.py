import os
import re

import sys

# user_database.csv structure:
# email, firstname, lastname, acct#, password, balance

# User database file
user_database = "data/user_database.csv"

# Session file
auth_session_file = "auth_session/current_session.txt"

# Complaint file
complaint_file = "data/complaints.txt"

# Error messages
error = "*** Error: "
file_not_found = error + "Could not access database. Exiting ATM. Goodbye."
io_error = error + "Could not write to database. Exiting ATM. Goodbye"


def create(email: str = "", firstname: str = "", lastname: str = "",
           acct_num: int = 0, password: str = "", balance: int = 0) -> bool:
    """
    Creates a new user entry in the database file
    :param email: user's email
    :param firstname: user's first name
    :param lastname: user's last name
    :param acct_num: user's account number
    :param password: user's password
    :param balance: user's account balance
    :return: True if successful, otherwise False
    """
    # Verify email address does not already exist
    # If it does, return False
    # If it does not, attempt to add account to database
    if append(user_database, f"\n{email},{firstname},{lastname},{acct_num},{password},{balance}"):
        return True
    else:
        sys.exit()


def update(new_details: dict) -> bool:
    """
    Update user details
    :param new_details: new user details
    :return: True if successful, otherwise False
    """
    user = new_details["email"]

    # Convert new details to string
    new_str = dict_to_str(new_details)

    # Get contents of database file
    lines = read(user_database)

    # Go through each line to find the "old" data, then replace with new data
    for x in range(len(lines)):
        if re.search(r"^" + user + r",", lines[x]):
            lines[x] = new_str
            lines = "\n".join(lines)

            # Update database file
            if write(user_database, lines):
                return True
            else:
                sys.exit()
    else:
        print("Could not update record!")
        return False


def delete(remove_user: str) -> bool:
    """
    Delete user from user database, adds user to closed account database
    :param remove_user: user to remove
    :return: True if successful, otherwise False
    """
    # Get contents of database file
    lines = read(user_database)

    # Go through each line to find the data
    for x in range(len(lines)):
        if re.search(r"^" + remove_user + ",", lines[x]):
            lines.pop(x)
            lines = "\n".join(lines)

            # Delete user from database
            if write(user_database, lines):
                return True
            else:
                sys.exit()
    else:
        print("Could not delete record!")
        return False


def find(key: str, criteria) -> list:
    """
    Search user details and return list results (dictionary of user details)
    :param key: key to search for
    :param criteria: search criteria
    :return: list of dictionaries with entries matching criteria (if any)
    """
    found = []
    parsed_lines = []

    # Get contents of database file
    lines = read(user_database)

    # Create list of accounts (dict) from database
    for x in lines:
        parsed_lines.append(str_to_dict(x))

    # Search each key for the criteria.
    # If found, add dictionary of details to list.
    for x in parsed_lines:
        if x[key] == criteria:
            found.append(x)

    # Return results
    return found


def read(file: str) -> list:
    """
    Opens database file and returns list of contents
    :return: list of contents of file
    """
    lines = []

    try:
        db = open(file, "r")
    except (FileNotFoundError, IOError):
        sys.exit(file_not_found)
    else:
        for x in db:
            lines.append(x.strip())
        db.close()
        return lines


def write(file: str, entry: str) -> bool:
    """
    Write the provided entry to the given file
    :param file: file to write to
    :param entry: entry to write to file
    :return: True if successful, otherwise False
    """
    try:
        f = open(file, "w")
        f.write(entry)
    except FileNotFoundError:
        print(file_not_found)
        return False
    except IOError:
        print(io_error)
        return False
    else:
        f.close()
        return True


def append(file: str, entry: str) -> bool:
    """
    Append the provided entry to the given file
    :param file: file to write to
    :param entry: entry to write to file
    :return: True if successful, otherwise False
    """
    try:
        f = open(file, "a")
        f.write(entry)
    except FileNotFoundError:
        print(file_not_found)
        return False
    except IOError:
        print(io_error)
        return False
    else:
        f.close()
        return True


def end_session():
    """
    Deletes the auth_session file
    """
    if os.path.exists(auth_session_file):
        try:
            os.remove(auth_session_file)
        except FileNotFoundError:
            print(error + "The session file does not exist.")


def str_to_dict(entry: str) -> dict:
    """
    Converts the csv string into a dictionary
    :param entry: the entry to parse
    :return: a dictionary with the user details
    """
    # Split provided entry by commas into a list
    details = entry.split(",")

    # Create dictionary with user details
    user_details = {"email"     : details[0], "firstname": details[1], "lastname": details[2],
                    "accountNum": int(details[3]), "password": details[4], "balance": int(details[5])
                    }
    return user_details


def dict_to_str(data: dict) -> str:
    """
    Convert dictionary to csv string
    :param data: dictionary to convert
    :return: csv string of dictionary contents
    """
    data = list(data.values())
    user_str = "{0},{1},{2},{3},{4},{5}".format(data[0], data[1], data[2], data[3], data[4], data[5])
    return user_str


def file_complaint(user: str, complaint: str, date: str) -> bool:
    """
    Saves complaint to complaint database
    :param user: User who filed complaint
    :param complaint: The complaint to file
    :param date: The date/time complaint was made
    :return: True if successful, otherwise False
    """
    if append(complaint_file, user + "," + date + "," + complaint + "\n"):
        return True
    else:
        print(error + "Could not save complaint.")
        return False
