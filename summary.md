# Restaurant Sales Dashboard – Project Summary

## 1. Problem Overview

The program reads `restaurant_sales.csv` (columns: `Date, Item, Category, Quantity, Price`), calculates **Sales = Quantity × Price**, and reports:

- Sales by category
- Top item by quantity and by revenue
- Sales by date, with the best day
- Charts for each report
- Invalid rows are skipped and a missing file is handled gracefully

---

## 2. How It Was Implemented

### Step 1: Loading the data (`load_data`)
- The CSV is read with `pd.read_csv(..., dtype=str)` so every value is first read as text. This lets me validate each row myself instead of letting Pandas guess types.
- `FileNotFoundError` is caught and the program prints `Error: File 'sales2025.csv' not found.` and exits cleanly (no traceback).
- Column names are stripped of spaces and checked against the required five columns.

### Step 2: Validating each row
- Each row is checked in turn: date, item/category, quantity, price.
- `pd.to_numeric(..., errors="coerce")` converts a bad number (such as `five`) to `NaN`, which I then detect.
- Invalid rows are skipped with a message such as
  `Warning: Row 8 skipped - Quantity must be a number.`
- The row number is the **file line number** (`index + 2`, because the header is line 1).
- Valid rows are collected into a new DataFrame and a `Sales` column (`Quantity * Price`) is added.

### Step 3: Reports using GroupBy
| Report | GroupBy used |
|---|---|
| Sales by category | `groupby("Category")["Sales"].sum()` |
| Top item by quantity | `groupby("Item")["Quantity"].sum()` then `idxmax()` |
| Top item by revenue | `groupby("Item")["Sales"].sum()` then `idxmax()` |
| Daily sales / best day | `groupby("Date")["Sales"].sum()` then `idxmax()` |

### Step 4: Charts (Matplotlib)
- Bar charts for category sales and item revenue, and a line chart for daily sales.
- Charts are saved as PNG files (`category_sales.png`, `item_revenue.png`, `daily_sales.png`) so the console is not blocked during testing.

### Step 5: Menu
1. Sales by category
2. Top items (also prints total sales)
3. Top items and daily sales

### Step 6: Output formatting
- A helper function `money()` prints whole numbers as `220` instead of `220.0`.
- The word `unit` or `units` is chosen based on the quantity (`1 unit`, `45 units`).

---

## 3. Test Case Results

| Test Case | Description | Result |
|---|---|---|
| 1 | Normal input, sales by category | Total Rs. 14740 |
| 2 | One-row file, top items | Total Rs. 220, Paneer Tikka (1 unit) |
| 3a | Extra row with `five` as quantity | Row 8 skipped with warning |
| 3b | Missing file `sales2025.csv` | Error message, clean exit |
| 4 | Top items and daily sales | Gulab Jamun (45 units), best day 2026-10-01 |

---

## 4. Difficulties Faced and How They Were Solved

1. **Test Cases 1 and 4 passed, but 2 and 3 failed.**
   The normal data worked, so the problem was in edge-case handling and exact output text, not in the calculations.

2. **A bad value changed the whole column type.**
   When Pandas reads a column containing `five`, the entire `Quantity` column becomes text, which breaks the calculations.
   *Solution:* read everything as strings (`dtype=str`) and convert each value safely with `pd.to_numeric(errors="coerce")`.

3. **Wrong row number in the warning.**
   The expected output says "Row 8", but the Pandas index of that row is 6 (index starts at 0 and the header is not counted).
   *Solution:* use `index + 2` to match the line number in the file.

4. **Exact message matching.**
   The test expects the exact text `Warning: Row 8 skipped - Quantity must be a number.` and `Error: File 'sales2025.csv' not found.` Even a small difference in punctuation or spacing fails the test.
   *Solution:* copied the messages exactly from the problem statement.

5. **Missing file crashed the program.**
   Without error handling, Pandas shows a long traceback.
   *Solution:* wrap the file reading in `try/except FileNotFoundError`.

6. **Menu option for Test Case 2.**
   "Top items" must also print `Total sales`, but Case 4 ("Top items and daily sales") does not show it.
   *Solution:* made them separate menu options, using a `show_total` flag.

7. **Number formatting.**
   Multiplying values can give floats such as `220.0`, but the expected output is `220`.
   *Solution:* the `money()` helper function removes the `.0`.

8. **Singular vs plural.**
   Case 2 expects `1 unit` while Case 4 expects `45 units`.
   *Solution:* choose the word based on the quantity.

9. **Charts blocking the program.**
   `plt.show()` pauses the console until the window is closed, which is awkward when running several tests.
   *Solution:* save the charts with `plt.savefig()` and close them with `plt.close()`.

---

## 5. What I Learned

- How to use Pandas for reading, cleaning and validating CSV data.
- How GroupBy is used to total data by category, item and date.
- Why input validation and error handling matter, and how test cases for invalid and boundary input expose problems that normal data hides.
- Output has to match the required format exactly, character for character.
- How to create charts with Matplotlib.

---

## 6. How to Run

```bash
pip install pandas matplotlib
python restaurant_sales.py
```

Enter the CSV file name when asked (for example `restaurant_sales.csv`), then choose a menu option.
