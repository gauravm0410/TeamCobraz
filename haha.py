import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import cufflinks as cf
import matplotlib

def tuple_to_list(nested_tuple):
    """Convert a nested tuple to a nested list."""
    if isinstance(nested_tuple, tuple):
        return [tuple_to_list(item) for item in nested_tuple]
    return nested_tuple  # Base case: return the item if it's not a tuple

# Example usage:
nested_tuple = ((1, 2), (3, (4, 5)), (6,))
nested_list = tuple_to_list(nested_tuple)
print(nested_list)



# Set the backend to TkAgg to open plots in separate windows
matplotlib.use('TkAgg')

# Enable cufflinks for offline mode
cf.go_offline()
tupple=()
nested_listt=tuple_to_list(tupple)
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

# Step 3: Group by category and sum amounts (ignoring Date column)
category_group = df.groupby('Category').sum(numeric_only=True).reset_index()

# Step 4: Generate Visualizations

# --- Pie Chart ---
plt.figure(figsize=(7, 7))
plt.pie(category_group['Amount'], labels=category_group['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Category-wise Contribution to Total Expenditure')
plt.show()  # Ensures the pie chart is displayed

# --- Bar Chart: Amount spent per day in a month ---
# Create day and month columns explicitly for clarity
df['DayOfMonth'] = df['Date'].dt.day
df['MonthNum'] = df['Date'].dt.month

daily_spending = df.groupby(['DayOfMonth', 'MonthNum']).sum(numeric_only=True).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='DayOfMonth', y='Amount', hue='MonthNum', data=daily_spending)
plt.title('Amount of Money Spent per Day in a Month')
plt.xlabel('Day of Month')
plt.ylabel('Amount Spent')
plt.show()  # Ensures the bar chart is displayed

# --- Bar Chart: Amount spent per month ---
monthly_spending = df.groupby('Month').sum(numeric_only=True).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='Month', y='Amount', data=monthly_spending)
plt.title('Amount of Money Spent per Month in a Year')
plt.xlabel('Month')
plt.ylabel('Amount Spent')
plt.show()  # Ensures the bar chart is displayed

# --- Stacked Bar Chart: Total expenditure per month by category ---
monthly_category_spending = df.groupby(['Month', 'Category']).sum(numeric_only=True).unstack().fillna(0)
monthly_category_spending.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Total Expenditure per Month by Category')
plt.ylabel('Amount Spent')
plt.xlabel('Month')
plt.show()  # Ensures the stacked bar chart is displayed

# --- Heat Map: Spending intensity by category and day of the week ---
heatmap_data = df.pivot_table(index='Day', columns='Category', values='Amount', aggfunc='sum', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
plt.title('Spending Intensity by Category and Day of the Week')
plt.show()  # Ensures the heat map is displayed

# --- Radar Chart: Compare multiple categories ---
categories = category_group['Category']
amounts = category_group['Amount']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=amounts, theta=categories, fill='toself'))
fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False, title="Spending Comparison Across Categories")
fig.show()  # Ensures the radar chart is displayed
