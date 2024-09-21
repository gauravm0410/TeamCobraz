import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import cufflinks as cf
import matplotlib
from expense_explorer import *


# Set the backend to TkAgg to open plots in separate windows
matplotlib.use('TkAgg')
''''''


# Create a nested list
oma = len(expense_explorer.amounts)
nested_list = []

for i in range(oma):
    small_list = []  # Initialize a new small_list for each iteration
    small_list.append(expense_explorer.dates[i])
    small_list.append(expense_explorer.categories[i])
    small_list.append(expense_explorer.amounts[i])
    nested_list.append(small_list)

# Enable cufflinks for offline mode
cf.go_offline()

# Step 1: Create the DataFrame and specify column names
df = pd.DataFrame(nested_list, columns=['Date', 'Category', 'Amount'])

# Step 2: Convert the 'Date' column to datetime type and create additional columns
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day_name()

# Step 3: Group by category and sum amounts (ignoring Date column)
category_group = df.groupby('Category').sum(numeric_only=True).reset_index()

# Step 4: Generate Visualizations

# --- Pie Chart ---
plt.figure(figsize=(7, 7))
plt.pie(category_group['Amount'], labels=category_group['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Category-wise Contribution to Total Expenditure')
plt.savefig('pie_chart.png')  # Save the pie chart
plt.show()  # Ensures the pie chart is displayed

# --- Bar Chart: Amount spent per day in a month ---
df['DayOfMonth'] = df['Date'].dt.day
df['MonthNum'] = df['Date'].dt.month

# Group by DayOfMonth and MonthNum, summing the 'Amount' for duplicate dates
daily_spending = df.groupby(['DayOfMonth', 'MonthNum'], as_index=False).agg({'Amount': 'sum'})

plt.figure(figsize=(10, 6))
sns.barplot(x='DayOfMonth', y='Amount', hue='MonthNum', data=daily_spending)
plt.title('Amount of Money Spent per Day in a Month')
plt.xlabel('Day of Month')
plt.ylabel('Amount Spent')
plt.savefig('bar_chart.png')
plt.show()

# --- Bar Chart: Amount spent per month ---
monthly_spending = df.groupby('Month').sum(numeric_only=True).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='Month', y='Amount', data=monthly_spending)
plt.title('Amount of Money Spent per Month in a Year')
plt.xlabel('Month')
plt.ylabel('Amount Spent')
plt.savefig('stacked_bar_chart.png')
plt.show()

# --- Heat Map: Spending intensity by category and day of the week ---
heatmap_data = df.pivot_table(index='Day', columns='Category', values='Amount', aggfunc='sum', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
plt.title('Spending Intensity by Category and Day of the Week')
plt.savefig('heatmap.png')
plt.show()
