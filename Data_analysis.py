import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/ahmed/Desktop/sales.csv")


print(df.head())
print(df.info())
print(df.describe())

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Check for missing values
print(df.isnull().sum())

# Add a calculated column: UnitPrice
df["UnitPrice"] = df["Revenue"] / df["Sales"]





# Sample data
df = pd.DataFrame({
    "Date": pd.date_range(start="2025-01-01", periods=5),
    "Revenue": [90, 125, 180, 150, 200]
})

# Plot line chart
plt.plot(df["Date"], df["Revenue"], marker='o')
plt.title("Revenue Over Time")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.grid(True)
plt.show()

df_products = pd.DataFrame({
    "Product": ["Apple", "Banana", "Orange"],
    "Sales": [90, 70, 50]
})

df_products.plot(kind="bar", x="Product", y="Sales", color="skyblue", legend=False)
plt.title("Sales by Product")
plt.ylabel("Sales")
plt.show()