"""
Used to test the budgets module
"""

from budgets import *

sep = "=" * 30 + "\n"

# Create categories
food_budget = Category("Food budget", 500)
clothes_budget = Category("Clothing budget", 300)
shoe_budget = Category("Shoe budget", 200)
car_budget = Category("Car budget", 200)
car_budget.set_category("My Car")
entertainment_budget = Category("Entertainment budget", 350)

print(sep)

# Deposit amounts
food_budget.deposit(50)
clothes_budget.deposit(80)

print(sep)

# Withdraw amounts
shoe_budget.withdraw(50)
car_budget.withdraw(80)

print(sep)

# Transfer amounts
clothes_budget.transfer(food_budget, 60)
entertainment_budget.transfer(car_budget, 100)

print(sep)

# Display category info
for x in (food_budget, car_budget, entertainment_budget):
    x.display_category()

print(sep)

# Add list of expenses
food_budget.add_expense_list([["Breakfast", 80], ["Lunch", 90],
                              ["Dinner", 100], ["Snacks", 50]])
clothes_budget.add_expense_list([["Shirts", 80], ["Pants", 120],
                                 ["Underwear", 50]])
shoe_budget.add_expense_list([["Sneakers", 120], ["Boots", 60]])
entertainment_budget.add_expense_list([["Games", 100], ["Movies", 60]])

# Add single expense
car_budget.add_expense("Gas", 80)

print(sep)

# Create copy of car budget
new_car_budget = car_budget.copy_category()
new_car_budget.set_category("New Car #2")

# Clear the new car budget
new_car_budget.clear_all_expenses()

# Display new car budget
new_car_budget.display_expenses()

print(sep)

# Create new collection
home_collection = Collection("Home")

# Add categories to Home collection
for budget in (food_budget, clothes_budget, shoe_budget, car_budget,
               entertainment_budget, new_car_budget):
    home_collection.add_category(budget)

print(sep)

# Display category names in Home collection
home_collection.display_category_names()

print(sep)

# Display category info in Home collection
home_collection.display_category_info()

print(sep)

# Copy home collection
copy_collection = home_collection.copy_collection()

# Remove a category from home
home_collection.remove_category("Shoe budget")

# Show copy was not affected by changes to home
copy_collection.display_collection()
print(sep)
home_collection.display_collection()

# # Check budget balances
# for budget in (food_budget, clothes_budget, shoe_budget, car_budget,
#                entertainment_budget, new_car_budget):
#     budget.display_category()
#     print(sep)
