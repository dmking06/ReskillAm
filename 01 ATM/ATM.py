import datetime

allowedUsers = ['Seyi', 'Mike', 'Love']
allowedPassword = ["passwordSeyi", "passwordMike", "passwordLove"]
menuOptions = [
    [1, "Withdrawal"],
    [2, "Cash Deposit"],
    [3, "Complaint"],
    [4, "Exit"],
    ]

returnMenu = "Returning to previous menu..."
prevMenu = "Enter \"Exit\" to return to previous menu.\n"

print("Welcome to the ATM.\n")
name = input("What is your name? ")

if name in allowedUsers:
    password = input("Your password? ")
    userId = allowedUsers.index(name)

    if password == allowedPassword[userId]:
        while 1:
            currentTime = datetime.datetime.now()
            print("\nWelcome {}!\nToday is {}"
                  .format(name, currentTime.strftime("%A, %d %B %Y %X")))
            print("Here are the available options:")
            for option in menuOptions:
                print("{}. {}".format(option[0], option[1]))

            selectOption = input("\nPlease select an option: ")

            if selectOption.isnumeric():
                selectOption = int(selectOption)
            else:
                print("*** Invalid menu selection. Please try again.")
                continue

            if selectOption == 1:
                withdraw = input("Input the amount to withdraw.\n"
                                 + prevMenu + "$").casefold()
                if withdraw.isnumeric():
                    print("Retrieving ${}...\nPlease take your cash."
                          .format(withdraw))
                    break
                elif withdraw == "exit":
                    print(returnMenu)
                else:
                    print("Invalid input. " + returnMenu)
            elif selectOption == 2:
                deposit = input("Input the amount to deposit.\n"
                                + prevMenu + "$").casefold()
                if deposit.isnumeric():
                    print("Depositing ${}...\n"
                          "Your balance is now ${:.2f}"
                          .format(deposit, int(deposit) + 360))
                    break
                elif deposit == "exit":
                    print(returnMenu)
                else:
                    print("Invalid input. " + returnMenu)
            elif selectOption == 3:
                complaint = input("Please enter your complaint.\n"
                                  + prevMenu).casefold()
                if complaint == "exit":
                    print(returnMenu)
                elif complaint != "exit":
                    print("Thank you for contacting us.")
                    break
            elif selectOption == 4:
                print("Thank you for using ATM. Have a good day.")
                break
            else:
                print("*** Invalid option selected; please try again.")
    else:
        print("*** Password incorrect; please try again.")
else:
    print("*** Name not found; please try again.")
