# Restaurant Sales Dashboard (PS 82)

A menu-driven Python program that reads a restaurant's sales data from a CSV file, cleans it, and shows sales summaries and charts using **Pandas** and **Matplotlib**.

Sales for each row is calculated as:

```
Sales = Quantity x Price
```

## Features

- Loads a CSV file and validates every row (invalid rows are skipped with a warning)
- Sales by category, with the total sales
- Top item by quantity sold and top item by revenue
- Day-wise sales and the best day
- Three charts (category, date, item) shown on screen and saved as `sales_charts.png`
- Friendly handling of a missing file, empty data and invalid menu choices

## Requirements

- Python 3
- pandas
- matplotlib

Install the libraries:

```bash
pip install pandas matplotlib
```

## Input File Format

The CSV file must have these columns:

| Column     | Description                      |
|------------|----------------------------------|
| `Date`     | Date of the sale (e.g. 2026-11-01) |
| `Item`     | Name of the item sold            |
| `Category` | Category of the item             |
| `Quantity` | Number of units sold (number)    |
| `Price`    | Price per unit (number)          |

Example `restaurant_sales.csv`:

```csv
Date,Item,Category,Quantity,Price
2026-11-01,Paneer Tikka,Starter,10,220
2026-11-01,Cold Coffee,Beverage,15,90
2026-11-02,Butter Naan,Bread,30,40
2026-11-02,Paneer Tikka,Starter,5,220
```

## How to Run

1. Put the CSV file in the same folder as the program.
2. Run the program (replace `main.py` with your file name):

   ```bash
   python main.py
   ```
3. Enter the CSV file name when asked:

   ```
   Enter file name (example: restaurant_sales.csv): restaurant_sales.csv
   ```
4. Choose an option from the menu.

## Menu Options

```
--- MENU ---
1. Sales by category
2. Top items
3. Top items and daily sales
4. Show charts
5. Exit
```

| Option | What it does |
|--------|--------------|
| 1 | Prints total sales for each category (highest first) and the overall total |
| 2 | Prints the top item by quantity and the top item by revenue |
| 3 | Prints the top items, then sales for each date and the best day |
| 4 | Displays three charts and saves them as `sales_charts.png` |
| 5 | Exits the program |

## Sample Output

For the example CSV above:

**Option 1**

```
Starter : Rs. 3300
Beverage : Rs. 1350
Bread : Rs. 1200
Total sales: Rs. 5850
```

**Option 3**

```
Top item by quantity: Butter Naan (30 units)
Top item by revenue: Paneer Tikka (Rs. 3300)
2026-11-01 : Rs. 3550
2026-11-02 : Rs. 2300
Best day: 2026-11-01
```

**Option 4** shows and saves these charts:

- Sales by Category (bar chart)
- Sales by Date (line chart)
- Revenue by Item (bar chart)

## Error Handling

| Situation | Behaviour |
|-----------|-----------|
| File not found | Prints `Error: File '<name>' not found.` and stops |
| `Quantity` is not a number | Prints `Warning: Row <n> skipped - Quantity must be a number.` |
| `Price` is not a number | Prints `Warning: Row <n> skipped - Price must be a number.` |
| No valid rows in the file | Prints `No valid rows found.` and stops |
| Wrong menu choice | Prints `Invalid choice, try again.` |

Row numbers in warnings match the row number in the CSV file, counting the header as row 1 (so the first data row is row 2).

## Code Structure

| Function | Purpose |
|----------|---------|
| `show(number)` | Formats numbers: `6300.0` is shown as `6300`, `6300.5` stays `6300.5` |
| `load_data(filename)` | Reads the CSV, validates each row, and adds the `Sales` column |
| `sales_by_category(data)` | Category-wise sales and total sales |
| `top_items(data)` | Top item by quantity and by revenue |
| `daily_sales(data)` | Date-wise sales and best day |
| `show_charts(data)` | Draws, saves and shows the charts |
| `main()` | Asks for the file name and runs the menu loop |

## Output Files

- `sales_charts.png` - image of the three charts, created when option 4 is used

## Notes

- All amounts are shown in rupees (`Rs.`).
- Dates are treated as text, so they are grouped exactly as written in the CSV. Use one consistent format (e.g. `YYYY-MM-DD`) so that days sort correctly.
