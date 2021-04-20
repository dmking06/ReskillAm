from budgets import Category

sep = "=" * 30 + "\n"

# Create categories
food_budget = Category("Food budget", 500)
clothes_budget = Category("Clothing budget", 300)
shoe_budget = Category("Shoe budget", 200)
car_budget = Category("Car budget", 200)
car_budget.set_name("My Car")
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
food_budget.add_expense_list([["Breakfast", 100], ["Lunch", 100],
                              ["Dinner", 100], ["Snacks", 100]])
clothes_budget.add_expense_list([["Shirts", 80], ["Pants", 120],
                                 ["Underwear", 50]])
shoe_budget.add_expense_list([["Sneakers", 120], ["Boots", 60]])
entertainment_budget.add_expense_list([["Games", 100], ["Movies", 60]])

# Add single expense
car_budget.add_expense("Gas", 80)

print(sep)

# Create copy of car budget
new_car_budget = car_budget.copy_category("Car #2")
new_car_budget.clear_all_expenses()

# Clear car budget
new_car_budget.display_expenses()

print(sep)

# Check budget balances
for budget in (food_budget, clothes_budget, shoe_budget, car_budget,
               entertainment_budget, new_car_budget):
    budget.display_category()
    print(sep)
