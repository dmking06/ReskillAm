"""
This module contains the following classes:
 - Budget - a template class
 - Category - creates a budget category
 - Collection - creates collection of categories
 - Expenses - creates a collection of expenses for categories
"""

_error = "*** Error: "
_dash_sep = "-" * 30
_star_sep = "*" * 30


class Budget:
    """
    Template budget class
    """

    def __init__(self):
        """
        Placeholder constructor
        """
        pass

    def deposit(self, amount: int):
        """
        Placeholder deposit method
        :param amount: Amount to deposit
        :return:
        """
        pass

    def withdraw(self, amount: int):
        """
        Placeholder withdraw method
        :param amount: Amount to withdraw
        :return:
        """
        pass

    def check_balance(self):
        """
        Placeholder check_balance method
        """
        pass

    def transfer(self, to_budget: "Budget", amount: int):
        """
        Placeholder transfer method
        :param to_budget: Budget to transfer to
        :param amount: Amount to transfer
        :return:
        """
        pass


class Category(Budget):
    """
    A budget category. Can hold an Expenses obj containing various expenses.
    """
    def __init__(self, category: str, amount: int, show_update: bool = True):
        """
        Create the budget category
        :param category: Name of the budget category
        :param amount: Max amount for the budget category
        :param show_update: Determines whether results are shown
        """
        super().__init__()
        try:
            self.category = category
            self.max_amount = self.balance = amount
            self.expenses = Expenses()
        except TypeError:
            print(_error + "category must be a string, and amount must be an"
                           " int.")
        except AttributeError:
            print(_error + "category must be a string!")
        else:
            if show_update:
                print("New budget category created: {}".format(category))

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
        calculate_percentage(self.category, self.balance, self.max_amount)

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

    def copy_category(self) -> "Category":
        """
        Create and return a copy of the category
        :return: A copy of the Category obj
        """
        copy = Category(self.category + " copy", self.max_amount, False)
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
        self.expenses = Expenses()
        self.balance = self.max_amount

    def display_expenses(self):
        """
        Displays the current expenses
        """
        print("Expenses in {}:".format(self.category))
        self.expenses.display_expenses()

    def display_category(self):
        """
        Display all expenses and balance of the category
        """
        self.display_expenses()
        self.check_balance()

    def set_category(self, category: str):
        """
        Set the name of the budget category
        :param category: Name to change to
        """
        self.category = category

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

    def get_category(self) -> str:
        """
        Get the category name
        :return: Category name
        """
        return self.category

    def get_max_amount(self) -> int:
        """
        Get the max amount of the category
        :return: Max amount
        """
        return self.max_amount

    def get_balance(self) -> int:
        """
        Get the current balance of the category
        :return: Balance amount
        """
        return self.balance

    def get_expenses(self) -> "Expenses":
        """
        Get the expenses of the category
        :return: Expenses obj
        """
        return self.expenses


class Collection:
    def __init__(self, name: str, show_update: bool = True):
        """
        Create a Collection obj. Collections can hold multiple categories
        :param name: Name of the Collection
        """
        self.name = name
        self.total_balance = 0
        self.total_max = 0
        self.categories = []
        if show_update:
            print("New Collection created: {}".format(self.name))

    def add_category(self, category: "Category", show_update: bool = True):
        """
        Add a Category obj to the Collection
        :param category: Category to add
        :param show_update: Determines whether results are shown
        """
        self.categories.append(category)
        self.total_max += category.get_max_amount()
        self.total_balance += category.get_balance()
        if show_update:
            print("Added category '{}' to {}"
                  .format(category.get_category(), self.name))

    def remove_category(self, name: str, show_results: bool = True):
        """
        Remove a Category obj from the collection by name
        :param name: Name of Category to remove
        :param show_results: Determines whether results are shown
        """
        for x in self.categories:
            if x.get_category() == name:
                self.categories.remove(x)
                self.total_max -= x.get_max_amount()
                self.total_balance -= x.get_balance()
                if show_results:
                    print("Removed category '{}' from '{}'"
                          .format(name, self.name))
                break
        else:
            print("Could not remove '{}' from '{}'".format(name, self.name))

    def clear_all_categories(self):
        """
        Remove all Categories from the Collection
        """
        del self.categories
        self.categories = []
        self.total_balance = 0
        self.total_max = 0
        print("Cleared all categories from '{}'".format(self.name))

    def display_category_names(self):
        """
        Display all of the Category names for the Collection
        """
        print("Categories in '{}':".format(self.name))
        for x in self.categories:
            print("  {}".format(x.get_category()))

    def display_category_info(self):
        """
        Show the details for each Category in the Collection
        """
        print("Category info in '{}':".format(self.name))
        for x in self.categories:
            x.display_category()
            print(_dash_sep)

    def display_collection_amount(self):
        """
        Display the balance amounts
        """
        calculate_percentage(self.name, self.total_balance, self.total_max)

    def display_collection(self):
        """
        Display all information for the Collection
        """
        print("{}\n{} Collection info:".format(_star_sep, self.name))
        self.display_collection_amount()
        self.display_category_info()

    def copy_collection(self) -> "Collection":
        """
        Create a copy of the Collection
        :return: A copy of the Collection
        """
        copy = Collection(self.name + " copy")
        for x in self.categories:
            copy.add_category(x.copy_category(), False)
        return copy

    def set_name(self, name: str):
        """
        Set the name of the Collection
        :param name: Name to set
        """
        self.name = name

    def set_total_max(self, amount: int):
        """
        Set the total max amount of the Collection
        :param amount: Amount to set
        """
        self.total_max = amount

    def get_total_balance(self) -> int:
        """
        Get the total balance of the collection
        :return: The total balance
        """
        return self.total_balance

    def get_total_max(self) -> int:
        """
        Get the total max amount for the collection
        :return: The total balance
        """
        return self.total_max

    def get_name(self) -> str:
        """
        Get the name of the collection
        :return: The name of the Collection
        """
        return self.name


class Expenses:
    def __init__(self):
        """
        Create an expense object for a budget category
        """
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
        Return a copy of the Expenses obj
        """
        copy = Expenses()
        copy.items = self.items.copy()
        return copy


def calculate_percentage(name: str, dividend: int, divisor: int):
    """
    Calculate percentage for collection/category
    :param name: Name of collection/category
    :param dividend: Used amount
    :param divisor: Total amount
    """
    descriptor = ["under", "over"]
    which = 0

    if divisor > 0:
        if dividend > 0:
            percentage = dividend / divisor * 100
            which = 0
        else:
            percentage = dividend / divisor * -100
            which = 1
    else:
        percentage = 0

    print("{} balance: ${} of ${} ({:.0f}% {})"
          .format(name, dividend, divisor, percentage, descriptor[which]))
