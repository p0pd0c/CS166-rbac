# csv is used to read/write to csv files
import csv

# used for matching strings to regex pattern
import re

# hides user's password as they type
import getpass

# used to exit the program if there is a fatal issue
import sys

# used to determine whether to use cls or clear to wipe the menu
from os import system, name

# used to delay for dramatic effect on your affect
from time import sleep


# reads username, password, and role from csv
# populates credential_dictionary
# csv structure:
# username,password,role
def parse_credentials(filename, credential_dictionary):
    # Wipe out credentials (in the case that we are creating creds and need to pick up on any additions)
    credential_dictionary.clear()

    # Read credentials
    with open(filename, newline='\n') as csvfile:
        cred_reader = csv.reader(csvfile)
        for row in cred_reader:
            # Username stored at index 0, password at index 1, and role at index 2
            credential_dictionary[row[0]] = (row[1], row[2])


# Check the dictionary for the username and password
# Returns authenticated:bool, username:str, and role:str
def check_credentials(username, password, credential_dictionary):
    # See if the username exists
    if username in credential_dictionary:
        # Verify Password, Password is the first element in the tuple
        if password == credential_dictionary[username][0]:
            # Role is the second element of the tuple
            return True, username, credential_dictionary[username][1]
    # User failed authentication
    return False, "", ""


# Save credentials to file
# Re-parse and return the credentials after modification
def create_credentials(filename, username, password, role, credential_dictionary):
    with open(filename, 'a') as csvfile:
        cred_writer = csv.writer(csvfile)
        cred_writer.writerow([username, password, role])
    parse_credentials(filename, credential_dictionary)


# Returns a boolean if isthisvalid validates on mode
def validate(isthisvalid, mode=""):
    if type(mode) is not str:
        return False

    if mode == 'menu-intranet':
        return -1 < isthisvalid < 3

    if mode == 'menu-directory':
        return -1 < isthisvalid < 4

    if type(isthisvalid) is str:
        if mode is 'text':
            # Check if text begins with either a letter or number and disallow ,./\ or if not between 3 and 20 chars
            return re.match(r"^[a-zA-Z0-9][^,./\\;]{2,20}$", isthisvalid) is not None
        if mode is 'role':
            if type(isthisvalid) is str:
                return re.match(r"^(admin|accountant|engineer)$", isthisvalid) is not None

    return False  # Invalid mode


# Prompt user for their username and password and return True if authenticated, False otherwise
# Wraps check_credentials with print statements and input
def login(credential_dictionary):
    username, password = get_username_password()

    # MULTIPLE RETURN (authenticated, username, role)
    return check_credentials(username, password, credential_dictionary)


# Display directory information
def menu(mode):
    if type(mode) is not str:
        sys.exit("Something terrible has happened")

    if mode == "login/signup":
        print("0. Login")
        print("1. Signup")
        print("2. exit")

        choice = 0
        try:
            choice = int(input("Enter choice [0, 1, 2]: "))
            while not validate(choice, "menu-intranet"):
                choice = int(input("Invalid choice, try again [0, 1, 2]: "))
        except ValueError as e:
            print("That is not a number! redirecting to login...")
            choice = 0

        return choice

    if mode == "directory":
        print("0. Top Secret Schematics")
        print("1. Budget")
        print("2. Backdoor")
        print("3. exit - No pun intended")
        choice = 3
        try:
            choice = int(input("Enter Choice [0, 1, 2, 3]: "))
            while not validate(choice, "menu-directory"):
                choice = int(input("Invalid choice, try again [0, 1, 2, 3]: "))
        except ValueError as e:
            print("That is not a number! exiting...")
            choice = 3
        return choice


# Wipes out the menu
def clear_menu():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def warn(text):
    bar = ""
    for i in range(len(text)):
        bar += "-"
    print(bar)
    print(text)
    print(bar)


def get_username_password():
    username = input("Username: ")
    while not validate(username, "text"):
        username = input("Username [really? must start with a letter and cannot contain ,./\\]: ")

    password = getpass.getpass("Password: ")
    while not validate(password, "text"):
        password = getpass.getpass("Password cannot not contain [,./\\]: ")

    return username, password


def get_login(credential_dictionary):
    # Give the user 3 chances to log in
    # After 3 failed attempts, wait 5 seconds and exit
    authenticated, username, role = login(credential_dictionary)
    attempts = 0
    if authenticated is False:
        while attempts < 2:
            if authenticated is False:
                clear_menu()
                print("Password Incorrect!")
                authenticated, username, role = login(credential_dictionary)
            attempts += 1

    if authenticated is False:
        clear_menu()
        warn("INVALID CREDENTIALS")
        sleep(5)
        sys.exit("Sorry for the inconvenience!")

    return authenticated, username, role


# Prompt user to sign up
def get_signup(credential_dictionary):
    warn("Create Account")
    username, password = get_username_password()

    role = input("Role: ")
    while not validate(role, "role"):
        role = input("Role [admin, accountant, engineer]: ")

    create_credentials("credentials.csv", username, password, role, credential_dictionary)


def get_directory(username, role):
    print("Hello", role, username)
    choice = menu("directory")
    while choice != 3:
        if choice == 0:
            if role == "engineer" or role == "admin":
                print("wr--r---- death_star_plans.txt\n\n")
            else:
                print("Hey, you need a hardhat to get in here!")
        if choice == 1:
            if role == "accountant" or role == "admin":
                print("wr--r---- do_not_show_to_the_irs.xlsx\n\n")
            else:
                print("Have you seen that really big book we keep around? We've just been hit with an inquiry. WAIT A MINUTE, you're not supposed to be here")
        if choice == 2:
            if role == "admin":
                print("--x------ $@*&!&(*#&.exe\n\n")
            else:
                print("You are not the one who knocks")
        sleep(2)
        choice = menu("directory")


def main():
    credentials = {}
    warn("intranet")
    parse_credentials('credentials.csv', credentials)

    choice = menu("login/signup")
    while choice != 2:
        if choice == 0:
            authenticated, username, role = get_login(credentials)
            clear_menu()
            get_directory(username, role)

        if choice == 1:
            get_signup(credentials)
        choice = menu("login/signup")


if __name__ == "__main__":
    main()

# https://www.geeksforgeeks.org/clear-screen-python/ <- Helpful with clearing the terminal to redisplay
# getpass is a cross platform library that hides the password as the user types
# in order for getpass to work, this file must be invoked from the terminal,
# if you test with an IDE/Debugger clear and getpass will not work... the TERM environment var must be set,
# please call from the command line!
