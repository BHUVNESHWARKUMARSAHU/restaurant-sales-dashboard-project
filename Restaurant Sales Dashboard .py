# Restaurant Sales Dashboard (PS 82)
# Sales = Quantity x Price

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def show(number):
    # show 6300.0 as 6300, but keep 6300.5 as it is
    if number == int(number):
        return str(int(number))
    return str(number)


def load_data(filename):
    # Step 1: try to open the file
    try:
        df = pd.read_csv(filename, dtype=str)
    except FileNotFoundError:
        print("Error: File '" + filename + "' not found.")
        return None

    # Step 2: check every row, keep only the good ones
    good_rows = []
    for i in range(len(df)):
        row = df.iloc[i]
        row_no = i + 2          # +1 for header, +1 because rows start at 1

        # Quantity must be a number
        try:
            qty = float(row["Quantity"])
            if pd.isna(qty):
                raise ValueError
        except (ValueError, TypeError):
            print("Warning: Row " + str(row_no) + " skipped - Quantity must be a number.")
            continue

        # Price must be a number
        try:
            price = float(row["Price"])
            if pd.isna(price):
                raise ValueError
        except (ValueError, TypeError):
            print("Warning: Row " + str(row_no) + " skipped - Price must be a number.")
            continue

        good_rows.append([row["Date"], row["Item"], row["Category"], qty, price])

    data = pd.DataFrame(good_rows, columns=["Date", "Item", "Category", "Quantity", "Price"])

    # Step 3: make the Sales column
    data["Sales"] = data["Quantity"] * data["Price"]
    return data


def sales_by_category(data):
    result = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    for name, value in result.items():
        print(name + " : Rs. " + show(value))
    print("Total sales: Rs. " + show(data["Sales"].sum()))


def top_items(data):
    by_qty = data.groupby("Item")["Quantity"].sum()
    by_rev = data.groupby("Item")["Sales"].sum()
    print("Top item by quantity: " + by_qty.idxmax() + " (" + show(by_qty.max()) + " unit" +
          ("" if by_qty.max() == 1 else "s") + ")")
    print("Top item by revenue: " + by_rev.idxmax() + " (Rs. " + show(by_rev.max()) + ")")


def daily_sales(data):
    by_date = data.groupby("Date")["Sales"].sum()
    for day, value in by_date.items():
        print(day + " : Rs. " + show(value))
    print("Best day: " + by_date.idxmax())


def show_charts(data):
    by_cat = data.groupby("Category")["Sales"].sum()
    by_date = data.groupby("Date")["Sales"].sum()
    by_item = data.groupby("Item")["Sales"].sum()

    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    by_cat.plot(kind="bar", color="orange")
    plt.title("Sales by Category")
    plt.ylabel("Rs.")

    plt.subplot(1, 3, 2)
    by_date.plot(kind="line", marker="o")
    plt.title("Sales by Date")
    plt.ylabel("Rs.")

    plt.subplot(1, 3, 3)
    by_item.plot(kind="bar", color="green")
    plt.title("Revenue by Item")
    plt.ylabel("Rs.")

    plt.tight_layout()
    plt.savefig("sales_charts.png")     # saves the picture too
    plt.show()


def main():
    filename = input("Enter file name (example: restaurant_sales.csv): ").strip()
    data = load_data(filename)
    if data is None:
        return                          # file not found, stop here
    if data.empty:
        print("No valid rows found.")
        return

    while True:
        print()
        print("--- MENU ---")
        print("1. Sales by category")
        print("2. Top items")
        print("3. Top items and daily sales")
        print("4. Show charts")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            sales_by_category(data)
        elif choice == "2":
            top_items(data)
        elif choice == "3":
            top_items(data)
            daily_sales(data)
        elif choice == "4":
            show_charts(data)
        elif choice == "5":
            break
        else:
            print("Invalid choice, try again.")


main()