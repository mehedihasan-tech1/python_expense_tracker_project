from expense import Expense
import calendar
import datetime


def main():
    print("Welcome to the expense tracker")
    expense_file_path = "expense.csv"
    budget = 2000

    # Get user input for expense
    expense = get_user_expense()
    print(expense)

    # write their expense to file
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print("Getting user Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount ($): "))
    print(f"you've ectered {expense_name}, {expense_amount}")

    expense_catagories = [
        "🍔Food",
        "🏠Home",
        "💼Work",
        "🎉Fun",
        "🎧Music"
    ]

    while True:
        print("Select a catagory: ")
        for i, category_name in enumerate(expense_catagories):
            print(f"{i+1}. {category_name}")

        value_range = f"[1 - {len(expense_catagories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_catagories)):
            selected_category = expense_catagories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category, Please try again")

        break


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving user Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print("sumarize expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) != 3:
                print("Bad line:", repr(line))
                continue
            expense_name, expense_amount, expense_category = parts
            print(expense_name, expense_amount, expense_category)
            line_expense = Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses by category 📊: ")
    for key, amount in amount_by_category.items():
        print(f"  {key} : ${amount:.2f}")

    total_spent = sum([expens.amount for expens in expenses])
    print(f"you've spent ${total_spent:.2f} this month")

    remaining_budget = budget - total_spent
    print(f"✅remaining budget ${remaining_budget:.2f} this month")

    # get the current date
    now = datetime.datetime.now()
    # get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    # calculate the remaining the number of days in the current month
    remaining_days = days_in_month - now.day
    print("Remaining days in the current month: ", remaining_days)
    daily_budget = remaining_budget / remaining_days
    print(green(f"🎯Budget Per Day: ${daily_budget:.2f}"))

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
