# --- Sales Forecasting Script ---
# Author: Ahmed
# Description: Clean sales data and forecast future sales using Prophet

import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# -------------------------------
# 1. Load Data
# -------------------------------
file_path = r"C:\Users\ahmed\Desktop\SaleData.csv"
data = pd.read_csv(file_path)

# Clean column names (remove hidden spaces)
data.columns = data.columns.str.strip()

# -------------------------------
# 2. Clean and Convert Data Types
# -------------------------------
# Remove commas and spaces from numeric columns and convert to float
data['Sale_total'] = (
    data['Sale_total']
    .replace({',': ''}, regex=True)
    .astype(str)
    .str.strip()
    .astype(float)
)

data['Unit_price'] = (
    data['Unit_price']
    .replace({',': ''}, regex=True)
    .astype(str)
    .str.strip()
    .astype(float)
)

# Convert OrderDate to datetime with explicit format
data['OrderDate'] = pd.to_datetime(data['OrderDate'], format='%m/%d/%y', errors='coerce')

# Drop rows where date parsing failed
data = data.dropna(subset=['OrderDate'])

# Set date as index
data.set_index('OrderDate', inplace=True)

# -------------------------------
# 3. Aggregate Monthly Sales
# -------------------------------
# Use 'ME' (month end) since 'M' is deprecated
monthly_sales = data.resample('ME')['Sale_total'].sum()

print("\n✅ Monthly Sales Data:")
print(monthly_sales.head())

# -------------------------------
# 4. Visualize Sales Trend
# -------------------------------
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales, marker='o')
plt.title("Monthly Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales ($)")
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------
# 5. Forecast with Prophet
# -------------------------------
df = monthly_sales.reset_index()
df.columns = ['ds', 'y']

model = Prophet()
model.fit(df)

# Forecast next 6 months
future = model.make_future_dataframe(periods=6, freq='M')
forecast = model.predict(future)

# -------------------------------
# 6. Plot Forecast Results
# -------------------------------
model.plot(forecast)
plt.title("Sales Forecast (Next 6 Months)")
plt.xlabel("Date")
plt.ylabel("Predicted Sales ($)")
plt.tight_layout()
plt.show()

# Optional: Decompose trends and seasonality
model.plot_components(forecast)
plt.tight_layout()
plt.show()

# -------------------------------
# 7. Print Summary
# -------------------------------
print("\n✅ Forecast complete!")
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(6))
