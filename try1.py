import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import numpy as np
import cufflinks as cf
import plotly.express as px

# Enable cufflinks for offline mode
cf.go_offline()

# Nested list with expense data: [Date, Category, Amount]
nested_list = [
    ['2024-01-01', 'Food', 50],
    ['2024-01-02', 'Transport', 20],
    ['2024-01-03', 'Entertainment', 70],
    ['2024-01-04', 'Rent', 1000],
    ['2024-01-05', 'Utilities', 100],
    ['2024-01-06', 'Food', 60],
    ['2024-01-07', 'Transport', 30]
]

# Step 1: Create the DataFrame and specify column names
df = pd.DataFrame(nested_list, columns=['Date', 'Category', 'Amount'])

# Step 2: Convert the 'Date' column to datetime type and create additional columns
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day_name()

# Group by category and sum amounts
category_group = df.groupby('Category').sum().reset_index()

# Step 3: Generate Visualizations

# --- Pie Chart ---
plt.figure(figsize=(7,7))
plt.pie(category_group['Amount'], labels=category_group['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Category-wise Contribution to Total Expenditure')
plt.show()

# --- Bar Chart: Amount spent per day in a month ---
daily_spending = df.groupby([df['Date'].dt.day, df['Date'].dt.month]).sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='Date', y='Amount', hue='Month', data=daily_spending)
plt.title('Amount of Money Spent per Day in a Month')
plt.xlabel('Day of Month')
plt.ylabel('Amount Spent')
plt.show()

# --- Bar Chart: Amount spent per month ---
monthly_spending = df.groupby('Month').sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='Month', y='Amount', data=monthly_spending)
plt.title('Amount of Money Spent per Month in a Year')
plt.xlabel('Month')
plt.ylabel('Amount Spent')
plt.show()

# --- Stacked Bar Chart: Total expenditure per month by category ---
monthly_category_spending = df.groupby(['Month', 'Category']).sum().unstack().fillna(0)
monthly_category_spending['Amount'].plot(kind='bar', stacked=True, figsize=(10,6))
plt.title('Total Expenditure per Month by Category')
plt.ylabel('Amount Spent')
plt.xlabel('Month')
plt.show()

# --- Heat Map: Spending intensity by category and day of the week ---
heatmap_data = df.pivot_table(index='Day', columns='Category', values='Amount', aggfunc='sum', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
plt.title('Spending Intensity by Category and Day of the Week')
plt.show()

# --- Radar Chart: Compare multiple categories ---
categories = category_group['Category']
amounts = category_group['Amount']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=amounts, theta=categories, fill='toself'))
fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False, title="Spending Comparison Across Categories")
fig.show()
