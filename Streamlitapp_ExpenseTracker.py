import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_PATH="Expense.csv"

def load_expenses():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["description","amount","category","purchase_date"])
    
def save_expenses(df):
    df.to_csv(FILE_PATH,index=False)

def add_expenses(df,desc,amount,cat,purchase_date):
    new = {"description": desc, "amount": float(amount),"category":cat,"purchase_date":purchase_date}
    return pd.concat([df,pd.DataFrame([new])],ignore_index=False)



st.title("Expense Tracker")

df = load_expenses()

menu = st.sidebar.radio("Menu", ["Add Expense", "View Expenses", "Filter by Category", "Summary", "Date Filter", "Monthly Report"])

if menu == "Add Expense":
    st.header("➕ Add New Expense")
    desc = st.text_input("Description")
    amount = st.number_input("Amount",min_value=0.0)
    cat = st.selectbox("Category",options=["Food","Transport","Utilities","Entertainment","Bathroom Essentials","Shopping","Fitness","Others"])
    purchase_date = st.date_input("Purchase_date",datetime.today())
    if st.button("Add Expense"):
        df = add_expenses(df,desc,amount,cat,purchase_date.strftime("%Y-%m-%d"))
        save_expenses(df)
        st.success("Expense Added!")

elif menu == "View Expenses":
    st.header("📋View Expenses")
    st.dataframe(df)

elif menu == "Filter by Category":
    st.header("🔍 Filter by Category")
    cat = st.selectbox("Select Category", df["category"].unique())
    filtered = df[df["category"]==cat]
    st.dataframe(filtered)

elif menu == "Summary":
    st.header("📊 Summary")
    total = df["amount"].sum()
    st.write(f"Total Spent: ${total:.2f}")
    category_sum = df.groupby("category")["amount"].sum()
    st.bar_chart(category_sum)

elif menu == "Date Filter":
    st.header("📆 Filter by Date Range")
    start = st.date_input("Start date")
    end = st.date_input("End date")

    if start and end:
        filtered_date = (pd.to_datetime(df["purchase_date"]) >= pd.to_datetime(start)) & (pd.to_datetime(df["purchase_date"]) <= pd.to_datetime(end))
        date_range=df[filtered_date]
        st.dataframe(date_range)
elif menu == "Monthly Report":
    st.header("📅 Monthly Expense Report")
    df["month"] = pd.to_datetime(df["purchase_date"]).dt.to_period("M").astype(str)
    monthly = df.groupby("month")["amount"].sum()
    st.bar_chart(monthly)



