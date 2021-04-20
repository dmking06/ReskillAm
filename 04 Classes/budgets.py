# Imagine we have a Categories of budgets e.g. Food Budget is one category, we can also have a Clothing category.
# Your task is to
# * Create a class "Category" and instantiate it with a different categories such as Food, Clothing and Car expenses
#   e.t.c (You can also add more) and their amounts.
# * Define the following methods in the class: Deposit, Withdraw, Transfer, Check Balance
#   (Feel free to add any other method)
#
#
# PS: Your solution must be dynamic and re-usable, it must support more budget in the future.
#
# What we'll look out for when grading are
# * Coding Conventions
# * Proper use of Data Structures

error = "*** Error: "


class Category:
    """
    A budget category. Holds an Expense obj containing various expenses.
    """
    def __init__(self, category: str, amount: int):
        """
        Create the budget category
        :param category: Name of the budget category
        :param amount: Max amount for the budget category
        """
        try:
            self.category = category
            self.max_amount = self.balance = amount
            self.expenses = Expenses(self.category)
        except TypeError:
            print(error + "category must be a string, and amount must be an "
                          "int.")
        except AttributeError:
            print(error + "category must be a string!")
        else:
            print("New budget created: {}".format(category))

    def deposit(self, deposit_amount: int, show_update: bool = True):
        """
        Add money to the category
        :param deposit_amount: Amount to add
        :param show_update: Determines whether results are shown
        """
        self.balance += deposit_amount
        if show_update:
            print(self.category, "amount after deposit: ", self.balance)

    def withdraw(self, withdrawal_amount: int, show_update: bool = True):
        """
        Subtract money from the category
        :param withdrawal_amount: Amount to subtract
        :param show_update: Determines whether results are shown
        """
        self.balance -= withdrawal_amount
        if show_update:
            print(self.category, "amount after withdrawal: ", self.balance)

    def check_balance(self):
        """
        Display the balance of the category
        """
        descriptor = ["left in budget", "over budget"]
        which = 0

        if self.max_amount > 0:
            if self.balance > 0:
                percentage = self.balance / self.max_amount * 100
                which = 0
            else:
                percentage = self.balance / self.max_amount * -100
                which = 1
        else:
            percentage = 0

        print("{} balance: ${} of ${} ({:.0f}% {})"
              .format(self.category, self.balance, self.max_amount,
                      percentage, descriptor[which]))

    def transfer(self, to_category: "Category", amount: int):
        """
        Transfer max budget amount to the given category
        :param to_category: Category to transfer to
        :param amount: Amount to transfer
        """
        print("Transferring ${} from {} to {}..."
              .format(amount, self.category, to_category.category))
        self.withdraw(amount, False)
        to_category.deposit(amount, False)
        self.check_balance()
        to_category.check_balance()

    def set_balance(self, amount: int):
        """
        Set the current balance
        :param amount: Amount to set
        """
        self.balance = amount

    def set_max_amount(self, amount: int):
        """
        Set the max budget amount
        :param amount: Amount to set
        """
        self.max_amount = amount

    def copy_category(self, copy_name: str) -> "Category":
        """
        Create and return a copy of the category
        :param copy_name: Name for the copy
        :return: A copy of the Category obj
        """
        copy = Category(copy_name, self.max_amount)
        copy.set_balance(self.balance)
        copy.expenses = self.expenses.copy_expenses()
        return copy

    def add_expense(self, name: str, amount: int, show_update: bool = True):
        """
        Add expense to budget category
        :param name: Name of expense
        :param amount: Amount of expense
        :param show_update: Determines whether results are shown
        """
        self.expenses.add(name, amount)
        self.withdraw(amount, False)
        if show_update:
            print("New expense added to {}:\n  {} - ${}"
                  .format(self.category, name, amount))

    def add_expense_list(self, expenses: list, show_update: bool = True):
        """
        Add list of expenses to budget category
        :param expenses: List of expenses to add
        :param show_update: Determines whether results are shown
        """
        print("New expenses added to {}:".format(self.category))
        for items in expenses:
            self.expenses.add(items[0], items[1])
            self.withdraw(items[1], False)
            if show_update:
                print("  {} - ${}".format(items[0], items[1]))

    def remove_expense(self, name: str, show_update: bool = True):
        """
        Remove an expense from the budget category
        :param name: Name of expense to remove
        :param show_update: Determines whether results are shown
        """
        removed_amount = self.expenses.remove(name)
        self.deposit(removed_amount, False)
        if show_update:
            print("Expense removed from {}:\n  {} - ${}"
                  .format(self.category, name, removed_amount))

    def clear_all_expenses(self):
        """
        Delete current Expense obj and create a new Expense obj
        """
        del self.expenses
        self.expenses = Expenses(self.category)
        self.balance = self.max_amount

    def display_expenses(self):
        """
        Displays the current expenses
        """
        print("Expenses in {}:".format(self.category))
        self.expenses.display_expenses()

    def set_name(self, category: str):
        """
        Set the name of the budget category
        :param category: Name to change to
        """
        self.category = category
        self.expenses.set_category(category)

    def display_category(self):
        """
        Display all expenses and balance of the category
        """
        self.display_expenses()
        self.check_balance()


class Expenses:
    def __init__(self, category: str):
        """
        Create an expense object for a budget category
        :param category: The budget category
        """
        self.category = category
        self.items = {}

    def add(self, name: str, amount: int):
        """
        Add a single expense
        :param name: Name of expense
        :param amount: Amount of expense
        """
        self.items.update({name: amount})

    def remove(self, name: str) -> int:
        """
        Remove a single expense by name
        :param name: Name of expense
        :return The amount of the expense removed
        """
        removed = self.items.pop(name)
        return removed

    def set_amount(self, name: str, amount: int, show_status: bool = True):
        """
        Set the amount of an expense by name
        :param name: Name of expense to adjust
        :param amount: New amount of expense
        :param show_status: Determines whether results are shown
        """
        self.items[name] = amount
        if show_status:
            print("New amount for {} expense: {}"
                  .format(name, self.items[name]))

    def set_category(self, category: str):
        """
        Set category for the Expense object
        :param category: Category for the Expense obj
        """
        self.category = category

    def set_name(self, old_name: str, new_name: str, show_status: bool = True):
        """
        Set the name of an expense
        :param old_name: Old expense name
        :param new_name: New expense name
        :param show_status: Determines whether results are shown
        """
        old_entry = self.items.pop(old_name)
        self.items.update({new_name: old_entry})
        if show_status:
            print("New name for {} expense: {}".format(old_name, new_name))

    def display_expenses(self):
        """
        Show all expenses for the category
        """
        if len(self.items) > 0:
            for key, value in self.items.items():
                print("  {} - ${}".format(key, value))
        else:
            print("  No expenses in this category.")

    def copy_expenses(self) -> "Expenses":
        """
        Return a copy of the Expense obj
        """
        copy = Expenses(self.category)
        copy.items = self.items.copy()
        return copy

