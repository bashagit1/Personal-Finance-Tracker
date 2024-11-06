import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Set up Streamlit app
st.set_page_config(page_title="💰 Personal Finance Tracker", page_icon="💸")

# Initialize session state for data storage
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount"])
if 'income' not in st.session_state:
    st.session_state.income = pd.DataFrame(columns=["Date", "Source", "Amount"])

# Sidebar for income/expense input
st.sidebar.header("💵 Log Your Income/Expense")

# Create columns for inputs
col1, col2 = st.columns(2)

# Income input
with col1:
    st.subheader("💼 Add Income")
    income_date = st.date_input("Income Date", datetime.date.today(), key="income_date")
    income_source = st.text_input("Income Source", placeholder="E.g., Salary")
    income_amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="income_amount")
    if st.button("✅ Log Income"):
        if income_source and income_amount > 0:
            new_income = pd.DataFrame({
                "Date": [income_date],
                "Source": [income_source],
                "Amount": [income_amount]
            })
            st.session_state.income = pd.concat([st.session_state.income, new_income], ignore_index=True)
            st.success(f"Income of ${income_amount:.2f} from {income_source} logged.")

# Expense input
with col2:
    st.subheader("💳 Add Expense")
    expense_date = st.date_input("Expense Date", datetime.date.today(), key="expense_date")
    expense_category = st.selectbox("Expense Category", ["Food 🍔", "Transport 🚗", "Entertainment 🎉", "Utilities 💡", "Others ❓"])
    expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="expense_amount")
    if st.button("❌ Log Expense"):
        if expense_category and expense_amount > 0:
            new_expense = pd.DataFrame({
                "Date": [expense_date],
                "Category": [expense_category],
                "Amount": [expense_amount]
            })
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
            st.success(f"Expense of ${expense_amount:.2f} for {expense_category} logged.")

# Financial Overview
st.header("📊 Financial Overview")
st.subheader("Income")
st.write(st.session_state.income)

st.subheader("Expenses")
st.write(st.session_state.expenses)

# Monthly Summary
if not st.session_state.income.empty and not st.session_state.expenses.empty:
    total_income = st.session_state.income['Amount'].sum()
    total_expenses = st.session_state.expenses['Amount'].sum()
    st.subheader("📅 Monthly Summary")
    st.write(f"Total Income: ${total_income:.2f}")
    st.write(f"Total Expenses: ${total_expenses:.2f}")

# Visualizations
if not st.session_state.expenses.empty:
    st.subheader("📈 Expenses by Category")
    expense_data = st.session_state.expenses.groupby('Category').sum().reset_index()
    
    # Bar chart for expenses
    plt.figure(figsize=(10, 5))
    plt.bar(expense_data['Category'], expense_data['Amount'], color='orange')
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    st.pyplot(plt)

    # Pie chart for expense breakdown
    st.subheader("🍕 Expense Breakdown")
    plt.figure(figsize=(8, 8))
    plt.pie(expense_data['Amount'], labels=expense_data['Category'], autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution")
    st.pyplot(plt)

# Export data
st.sidebar.header("📤 Export Data")
if st.sidebar.button("Download Income Data"):
    st.download_button(label="Download Income Data", data=st.session_state.income.to_csv(index=False).encode('utf-8'), file_name='income_data.csv')
if st.sidebar.button("Download Expense Data"):
    st.download_button(label="Download Expense Data", data=st.session_state.expenses.to_csv(index=False).encode('utf-8'), file_name='expense_data.csv')

# Additional tools section
st.sidebar.header("🛠️ Additional Tools")
if st.sidebar.button("Set Budget"):
    st.sidebar.subheader("Set Your Budget")
    budget_amount = st.sidebar.number_input("Set your budget amount", min_value=0.0, format="%.2f")
    if budget_amount > 0:
        st.sidebar.success(f"Budget of ${budget_amount:.2f} set!")

# Note: Further enhancements can be implemented as per user requirements.
