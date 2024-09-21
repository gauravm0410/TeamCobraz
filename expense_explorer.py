
import mysql.connector
from datetime import date
from collections import defaultdict



# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Parneeca2011"
)

# Prompt user for the budget and calculate daily and emergency budget
monthly_budget = float(input("Enter your monthly budget: "))
daily_budget = (monthly_budget / 30.0)*0.8 # 80% for daily use
emergency_fund = 0.2 * monthly_budget     # 20% for emergency use
saved_up = 0  # To track savings if expenditure is below daily budget

# Set up cursor and database
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS expenseexplorer")
mycursor.execute("USE expenseexplorer")
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS transactiontable(
        transid VARCHAR(255) PRIMARY KEY, 
        category VARCHAR(255), 
        amt DOUBLE(10,2), 
        item VARCHAR(255), 
        transaction_date DATE
    )
""")

# Function to insert transactions
'''while True:
    l1 = []  # Reset the list for every transaction
    cat = input("Enter category of expenditure: ")
    amount = float(input("Enter cost of purchase: "))
    item = input("Enter item name: ")
    current_date = date.today()
    current_date_string=str(current_date)

    l1.append(cat)
    l1.append(amount)
    l1.append(item)
    l1.append(current_date_string)
    
    tup = tuple(l1)'''
amounts = []
dates = []
transaction_ids = [] 
categories = []
items = []

file_path = 'extended_transaction_details.txt'

# Open and read the transaction file
with open(file_path, 'r') as file:
    for line in file:
        l1 = line.strip().split(",")
        print(l1)
        tup=tuple(l1)
        print(tup)
        # Split each line by comma to extract relevant fields
        txn_id, amount, date, item, category = line.strip().split(', ')
        
        # Append data to the corresponding lists
        amounts.append(int(amount))         # Convert amount to integer
        dates.append(date)                  # Dates as strings
        transaction_ids.append(txn_id)      # Store only transaction ID
        categories.append(category)         # Categories as strings
        items.append(item)                  # Items as strings

    
    sql = "INSERT INTO transactiontable(transid, amt, transaction_date, item, category) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(sql, tup)
    mydb.commit()

   
# Route to handle form submission

# Function to get distinct categories
def categories_func():
    mycursor.execute("SELECT DISTINCT category FROM transactiontable")
    categories_data = mycursor.fetchall()
    categories_list = [item[0] for item in categories_data]  # Extract first element from each tuple
    return categories_list

# Fetch daily expenditure and reset if the date changes


'''if __name__ == '__main__':
    app.run(debug=True, port=5050)'''

def items_func():
    mycursor.execute("SELECT item, amt FROM transactiontable")
    items_data = mycursor.fetchall()
    items_list= [item[0] for item in items_data]
    return items_list

