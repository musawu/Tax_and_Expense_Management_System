import calendar
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu














# Settings
incomes = {"Salary": 0, "Blog": 0, "Other Income": 0}
expenses = {
    "Rent": 0,
    "Utilities": 0,
    "Groceries": 0,
    "Car": 0,
    "Other Expenses": 0,
    "Saving": 0,
}
currency = "USD"
page_title = "Taxes and Expense Management System"
page_icon = ":money_with_wings:"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + "" + page_icon)




# Initialize years and months
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

hide_st_style = """<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;} </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# NAVIGATION MENU
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"], orientation="horizontal",
)

# Define a function to calculate total income after tax
def calculate_income_after_tax(incomes, tax_rate):
    return {income: amount * (1 - tax_rate) for income, amount in incomes.items()}

# Input & Save Periods
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month: ", months, key="month")
        col2.selectbox("Select Year:", years, key="year")
        with st.expander("Income"):
            for income in incomes:
                incomes[income] = st.number_input(
                    f" {income}:", min_value=0, format="%i", step=10, key=income
                )
        with st.expander("Expenses"):
            for expense in expenses:
                expenses[expense] = st.number_input(
                    f" {expense}:", min_value=0, format="%i", step=10, key=expense
                )

        with st.expander("Comment"):
            Comment = st.text_area("", placeholder="Enter a comment here ")

        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            # Save values into session state
            st.session_state["incomes"] = incomes
            st.session_state["expenses"] = expenses
            st.session_state["period"] = period
            st.session_state["Comment"] = Comment
            st.success("Data saved!")

# Data Visualization
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        # Retrieve periods from session state
        period = st.selectbox("Select Period:", [st.session_state["period"]])
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            # Retrieve data from session state
            incomes = st.session_state["incomes"]
            expenses = st.session_state["expenses"]
            Comment = st.session_state["Comment"]
            # Calculate total income after tax
            tax_rate = 0.2 # Example tax rate, you can adjust this
            incomes_after_tax = calculate_income_after_tax(incomes, tax_rate)

            # Create metrics
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            total_income_after_tax = sum(incomes_after_tax.values())
            total_tax = total_income - total_income_after_tax
            remaining_budget = total_income_after_tax - total_expense

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Total Tax", f"{total_tax} {currency}")
            col4.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comment: {Comment}")

            # Create sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")

            data = go.Sankey(link=link, node=node)
            # Plot it!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
