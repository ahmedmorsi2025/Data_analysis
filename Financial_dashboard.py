import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
from prophet import Prophet
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Multi-Company Financial Dashboard with AI Forecasting")

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect("financial_system.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS revenue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    amount REAL,
    company TEXT DEFAULT 'Company A'
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    amount REAL,
    company TEXT DEFAULT 'Company A'
)
""")
conn.commit()

# -------------------------------
# INSERT SAMPLE DATA IF EMPTY
# -------------------------------
companies = ["Company A", "Company B"]

for company in companies:
    cursor.execute("SELECT COUNT(*) FROM revenue WHERE company=?", (company,))
    if cursor.fetchone()[0] == 0:
        rev_data = [
            (2020, np.random.randint(10000,15000), company),
            (2021, np.random.randint(12000,16000), company),
            (2022, np.random.randint(14000,18000), company),
            (2023, np.random.randint(16000,20000), company),
            (2024, np.random.randint(17000,21000), company),
        ]
        exp_data = [
            (2020, np.random.randint(7000,10000), company),
            (2021, np.random.randint(8000,11000), company),
            (2022, np.random.randint(9000,12000), company),
            (2023, np.random.randint(10000,13000), company),
            (2024, np.random.randint(11000,14000), company),
        ]
        cursor.executemany("INSERT INTO revenue (year,amount,company) VALUES (?,?,?)", rev_data)
        cursor.executemany("INSERT INTO expenses (year,amount,company) VALUES (?,?,?)", exp_data)
conn.commit()

# -------------------------------
# COMPANY SELECTION
# -------------------------------
st.subheader("🏢 Select Company")
company = st.selectbox("Company", companies)

# -------------------------------
# LOAD DATA
# -------------------------------
revenue_df = pd.read_sql(
    "SELECT year, amount FROM revenue WHERE company=? ORDER BY year",
    conn, params=(company,)
)
expenses_df = pd.read_sql(
    "SELECT year, amount FROM expenses WHERE company=? ORDER BY year",
    conn, params=(company,)
)

data_df = revenue_df.copy()
data_df["Expenses"] = expenses_df["amount"]
data_df["Profit"] = data_df["amount"] - data_df["Expenses"]

# -------------------------------
# YEAR FILTER
# -------------------------------
min_year = int(data_df["year"].min())
max_year = int(data_df["year"].max())
selected_years = st.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)
filtered_df = data_df[
    (data_df["year"] >= selected_years[0]) &
    (data_df["year"] <= selected_years[1])
]

# -------------------------------
# DATA TABLE
# -------------------------------
st.subheader("📥 Financial Data")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# 3D CHARTS
# -------------------------------
st.subheader("📈 Financial Performance (3D)")
years = filtered_df["year"].values
revenues = filtered_df["amount"].values
expenses = filtered_df["Expenses"].values
profits = filtered_df["Profit"].values

fig_3d = go.Figure()
for i in range(len(years)):
    fig_3d.add_trace(go.Scatter3d(
        x=[years[i], years[i]],
        y=["Revenue", "Revenue"],
        z=[0, revenues[i]],
        mode="lines", line=dict(width=12),
        name="Revenue" if i==0 else None, showlegend=i==0
    ))
    fig_3d.add_trace(go.Scatter3d(
        x=[years[i], years[i]],
        y=["Expenses", "Expenses"],
        z=[0, expenses[i]],
        mode="lines", line=dict(width=12),
        name="Expenses" if i==0 else None, showlegend=i==0
    ))
    fig_3d.add_trace(go.Scatter3d(
        x=[years[i], years[i]],
        y=["Profit", "Profit"],
        z=[0, profits[i]],
        mode="lines", line=dict(width=12),
        name="Profit" if i==0 else None, showlegend=i==0
    ))
fig_3d.update_layout(
    title=f"3D Financial Overview ({company})",
    scene=dict(xaxis_title="Year", yaxis_title="Category", zaxis_title="Amount ($)"),
    height=600
)
st.plotly_chart(fig_3d, use_container_width=True)

# -------------------------------
# PIE CHART
# -------------------------------
st.subheader("💰 Expense Distribution")
labels = ["Salaries", "Rent", "Utilities", "Marketing", "Other"]
values = [4500, 2500, 1200, 1800, 1000]
fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
fig_pie.update_layout(title=f"Expense Breakdown ({company})")
st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------
# EXPLANATION
# -------------------------------
st.subheader("📝 Financial Analysis Explanation")
st.markdown(f"""
**Company:** {company}  
- Revenue trend over selected years: {'upward' if revenues[-1]>revenues[0] else 'flat/decline'}  
- Expenses trend: {'upward' if expenses[-1]>expenses[0] else 'flat/decline'}  
- Profit trend: {'increasing' if profits[-1]>profits[0] else 'flat/decline'}  
""")

# -------------------------------
# AI FORECASTING
# -------------------------------
st.subheader("🤖 AI Forecasting")

if len(filtered_df) >= 2:
    # Prophet Forecast
    df_prophet = filtered_df[["year","amount"]].rename(columns={"year":"ds","amount":"y"})
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], format="%Y")
    model = Prophet(yearly_seasonality=False, daily_seasonality=False)
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=1, freq='Y')
    forecast = model.predict(future)
    next_year = forecast.iloc[-1]
    predicted_revenue = next_year["yhat"]

    st.metric(label=f"Predicted Revenue (Prophet) for {int(forecast['ds'].dt.year.iloc[-1])}", value=f"${predicted_revenue:,.2f}")

    # Optional: Linear Regression Forecast
    X = filtered_df['year'].values.reshape(-1,1)
    y = filtered_df['amount'].values
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    next_year_lr = np.array([[filtered_df['year'].max() + 1]])
    predicted_lr = lr_model.predict(next_year_lr)[0]
    st.metric(label=f"Predicted Revenue (Linear Regression)", value=f"${predicted_lr:,.2f}")

else:
    st.info("Select at least two years to enable AI forecasting.")

conn.close()
