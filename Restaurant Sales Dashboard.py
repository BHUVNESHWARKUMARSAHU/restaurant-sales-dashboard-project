import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_NAME = "restaurant_sales.csv"


def load_data():
    if not os.path.exists(FILE_NAME):
        print(f"Error: File '{FILE_NAME}' not found.")
        return None

    try:
        df = pd.read_csv(FILE_NAME, dtype=str)
    except Exception as e:
        print("Error reading CSV file:", e)
        return None

    required_columns = ["Date", "Item", "Category", "Quantity", "Price"]

    if not all(col in df.columns for col in required_columns):
        print("Error: CSV file has missing columns.")
        return None

    valid_rows = []

    for index, row in df.iterrows():
        row_number = index + 2

        try:
            date = pd.to_datetime(row["Date"], format="%Y-%m-%d", errors="raise")
            item = str(row["Item"]).strip()
            category = str(row["Category"]).strip()
            quantity = float(row["Quantity"])
            price = float(row["Price"])

            if not item or not category:
                raise ValueError("Item or Category is empty")

            if quantity <= 0 or price < 0:
                raise ValueError("Quantity or Price is invalid")

            valid_rows.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Item": item,
                "Category": category,
                "Quantity": quantity,
                "Price": price,
                "Sales": quantity * price
            })

        except (ValueError, TypeError):
            print(
                f"Warning: Row {row_number} skipped - "
                "Invalid date, item, category, quantity or price."
            )

    if not valid_rows:
        print("No valid sales records found.")
        return pd.DataFrame(
            columns=required_columns + ["Sales"]
        )

    return pd.DataFrame(valid_rows)


def sales_by_category(df):
    if df.empty:
        print("No data available.")
        return

    result = df.groupby("Category")["Sales"].sum()

    print("\n--- SALES BY CATEGORY ---")

    for category, sales in result.items():
        print(f"{category} : Rs. {sales:.0f}")

    print(f"Total sales: Rs. {df['Sales'].sum():.0f}")


def sales_by_item(df):
    if df.empty:
        print("No data available.")
        return

    result = df.groupby("Item")["Sales"].sum()

    print("\n--- SALES BY ITEM ---")

    for item, sales in result.items():
        print(f"{item} : Rs. {sales:.0f}")


def top_items(df):
    if df.empty:
        print("No data available.")
        return

    quantity_data = df.groupby("Item")["Quantity"].sum()
    revenue_data = df.groupby("Item")["Sales"].sum()

    top_quantity = quantity_data.idxmax()
    top_revenue = revenue_data.idxmax()

    print("\n--- TOP SELLING ITEMS ---")

    print(
        f"Top item by quantity: {top_quantity} "
        f"({quantity_data[top_quantity]:g} units)"
    )

    print(
        f"Top item by revenue: {top_revenue} "
        f"(Rs. {revenue_data[top_revenue]:.0f})"
    )


def daily_sales(df):
    if df.empty:
        print("No data available.")
        return

    result = df.groupby("Date")["Sales"].sum()

    print("\n--- DAILY SALES ---")

    for date, sales in result.items():
        print(f"{date} : Rs. {sales:.0f}")

    best_day = result.idxmax()
    print(f"Best day: {best_day}")


def show_charts(df):
    if df.empty:
        print("No data available for charts.")
        return

    category_sales = df.groupby("Category")["Sales"].sum()
    daily = df.groupby("Date")["Sales"].sum()
    item_sales = df.groupby("Item")["Sales"].sum()

    plt.figure(figsize=(8, 5))
    category_sales.plot(kind="bar")
    plt.title("Restaurant Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales (Rs.)")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    daily.plot(kind="line", marker="o")
    plt.title("Daily Restaurant Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales (Rs.)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    item_sales.plot(kind="bar")
    plt.title("Sales by Item")
    plt.xlabel("Item")
    plt.ylabel("Revenue (Rs.)")
    plt.tight_layout()
    plt.show()


def main():
    print("===================================")
    print("     RESTAURANT SALES DASHBOARD")
    print("===================================")

    df = load_data()

    if df is None:
        return

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Sales by Category")
        print("2. Sales by Item")
        print("3. Top Items")
        print("4. Daily Sales")
        print("5. Show Charts")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            sales_by_category(df)

        elif choice == "2":
            sales_by_item(df)

        elif choice == "3":
            top_items(df)

        elif choice == "4":
            daily_sales(df)

        elif choice == "5":
            show_charts(df)

        elif choice == "6":
            print("Thank you for using Restaurant Sales Dashboard!")
            break

        else:
            print("Invalid choice! Please enter 1 to 6.")


if __name__ == "__main__":
    main()