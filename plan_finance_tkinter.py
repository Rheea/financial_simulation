from dataclasses import dataclass

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Note: This approach is ugly in code and GUI, but works like a charm

# Sanity checks done with: 
# https://www.thecalculatorsite.com/finance/calculators/savings-calculators.php#google_vignette

@dataclass
class FinanceHistory:
    years: np.ndarray[int]
    income: list
    expenses: list
    disposable: list
    savings: list
    investments: list
    investment_gains: list

def calculate_projection(
        age,
        investments,
        monthly_income,
        monthly_expenses,
        monthly_savings,
        inflation,
        salary_increase,
        roi,
        retirement_age,
        retirement_expenses_ratio, 
        life_expectancy,
        ):
    print(f"""Calculating Projection for values:
        Age: {age}, 
        Initial Inestments: {investments}, 
        Monthly Income: {monthly_income}, 
        Monthly Expenses: {monthly_expenses}, 
        Monthly Savings: {monthly_savings}, 
        Inflation Rate: {inflation}, 
        Salary Increase: {salary_increase}, 
        Return on Ivestments: {roi}, 
        Retirement Age: {retirement_age},
        % of Expenses at Retirement: {retirement_expenses_ratio},
        Life Expectancy: {life_expectancy}""")
    
    years = np.arange(age+1, life_expectancy + 1)

    # Adjust to yearly values
    income = monthly_income*12
    expenses = monthly_expenses*12
    savings = monthly_savings*12    

    # Transform percentages into ratios
    inflation = inflation/100
    salary_increase = salary_increase/100
    roi = roi/100

    
    # Init variables
    finance_history = FinanceHistory(
        years = years,
        income = [income],
        expenses = [expenses],
        disposable = [income - expenses],
        savings = [savings],
        investments = [investments],
        investment_gains = [0]    
    )        

    for year in years:
        # Calculate salary growth: grow by salary_increase rate or inflation if salary_increase is zero
        current_income = finance_history.income[-1] * (1 + salary_increase + inflation) 

        # Calculate how much is saved every year from income, following the same rate of increase as salary
        current_savings = finance_history.savings[-1] * (1 + salary_increase + inflation) 

        # Calculate expenses growth with inflation
        current_expenses = finance_history.expenses[-1] * (1 + inflation)
        
        # Calculate extra savings added to investments
        disposable = current_income - current_expenses - current_savings

        # Update investmetns with return on investment
        current_investments = finance_history.investments[-1] * (1+roi)

        investment_gains = current_investments - finance_history.investments[-1]
    
        # Change behaviour after retirement
        if year == retirement_age:
            # expenses half, but they will still grow with inflation
            current_expenses = current_expenses * retirement_expenses_ratio

        if year >= retirement_age:        
            current_income = 0
            current_savings = 0
            disposable = investment_gains - current_expenses
            
            # Update Investments by substracting inflation adjusted expenses, but keeping the 
            current_investments =  current_investments - current_expenses
        else:
            # Update Investments by adding savings
            current_investments = current_investments + current_savings
        
        # Save variables for plotting
        finance_history.income.append(current_income)        
        finance_history.expenses.append(current_expenses)
        finance_history.investments.append(current_investments)
        finance_history.investment_gains.append(investment_gains)
        finance_history.savings. append(current_savings)
        finance_history.disposable.append(disposable)

    return finance_history

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    print('onpick points:', *zip(xdata[ind], ydata[ind]))


def generate_graph():
    # Retrieve input values
    try:
        age = int(age_entry.get())
        investments = float(investments_entry.get())
        monthly_income = float(monthly_income_entry.get())
        monthly_expenses = float(monthly_expenses_entry.get())
        monthly_savings = float(monthly_savings_entry.get())
        inflation = inflation_slider.get()
        salary_increase = salary_increase_slider.get()
        roi = roi_slider.get()
        retirement_age = int(retirement_age_entry.get())
        retirement_expenses_ratio = float(retirement_expenses_ratio_entry.get())
        life_expectancy = int(life_expectancy_entry.get())
    except ValueError:
        result_label.config(text="Invalid input. Please check your entries.")
        return
        
    # Calculate Financial Projections
    finance_history = calculate_projection(
        age,
        investments,
        monthly_income,
        monthly_expenses,
        monthly_savings,
        inflation,
        salary_increase,
        roi,
        retirement_age,
        retirement_expenses_ratio,
        life_expectancy,
        )
    

    # Draw/Update Graph
    fig.clear()
    X_axis = np.arange(len(finance_history.years)+1) + min(finance_history.years)
    ax0 = fig.add_subplot(211)
    ax0.bar(X_axis - 0.4, finance_history.income, 0.2, label = 'Income')
    ax0.bar(X_axis - 0.2, finance_history.expenses, 0.2, label = 'Expenses')
    ax0.bar(X_axis + 0.0, finance_history.savings, 0.2, label = 'Savings') 
    ax0.bar(X_axis + 0.2, finance_history.disposable, 0.2, label = 'Disposable')
    ax0.bar(X_axis + 0.4, finance_history.investment_gains, 0.2, label = 'Investment Gains')    
    ax0.grid()
    ax0.legend()

    ax1 = fig.add_subplot(212)
    ax1.bar(X_axis - 0.2, finance_history.investments, label='Accumulated Investments')        
    ax1.grid()
    ax1.legend()
    
    fig.suptitle('Financial Projection')



    fig.canvas.mpl_connect('pick_event', onpick)
    canvas.draw()
    result_label.config(text="Graph updated!")

# Create the main window
root = tk.Tk()
root.title("Financial Projection Tool")

# Input fields and sliders
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Text input fields
fields = {
    "Age": (40, "age_entry"),
    "Investments": (20000, "investments_entry"),
    "Monthly Income": (7000, "monthly_income_entry"),
    "Monthly Expenses": (5000, "monthly_expenses_entry"),
    "Monthly Savings": (1000, "monthly_savings_entry"),
    "Retirement Age": (67, "retirement_age_entry"),
    "Retirement Expenses Ratio": (0.5, "retirement_expenses_ratio_entry"),
    "Life Expectancy": (85, "life_expectancy_entry"),
    
}
entries = {}
for i, (label_text, (default, variable_name)) in enumerate(fields.items()):
    label = ttk.Label(frame, text=f"{label_text}:")
    label.grid(row=i, column=0, sticky="w", pady=2)
    entry = ttk.Entry(frame)
    entry.grid(row=i, column=1, pady=2)
    entry.insert(0, default)
    entries[variable_name] = entry
globals().update(entries)  # Update variables dynamically

# Sliders
slider_frame = ttk.Frame(root)
slider_frame.pack(padx=10, pady=10)

inflation_slider = tk.Scale(slider_frame, from_=0, to=10, resolution=0.1, label="Inflation (%)", orient="horizontal")
inflation_slider.set(2.5)
inflation_slider.pack(side="left", padx=5)

salary_increase_slider = tk.Scale(slider_frame, from_=-5, to=5, resolution=0.1, label="Salary Increase (%)", orient="horizontal")
salary_increase_slider.set(1.0)
salary_increase_slider.pack(side="left", padx=5)

roi_slider = tk.Scale(slider_frame, from_=0, to=15, resolution=0.1, label="ROI (%)", orient="horizontal")
roi_slider.set(6.0)
roi_slider.pack(side="left", padx=5)

# Matplotlib figure
fig = Figure(figsize=(10,8), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(padx=10, pady=10)

# Generate graph button
button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=5)

generate_button = ttk.Button(button_frame, text="Generate Graph", command=generate_graph)
generate_button.pack()

# Result label
result_label = ttk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()
