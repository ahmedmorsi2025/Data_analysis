import pandas as pd

# Use raw string (r"") to avoid issues with backslashes in Windows paths
file_path = r"C:\Users\ahmed\Desktop\SaleData.csv"
data = pd.read_csv(file_path)

print(data.head())
print(data.info())

data['OrderDate'] = pd.to_datetime(data['OrderDate'])
data.set_index('OrderDate', inplace=True)

monthly_sales = data.resample('M')['Sale_total'].sum()
print(monthly_sales.head())

