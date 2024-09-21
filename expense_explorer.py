from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date
#app = Flask(__name__)


'''@app.route('/')
def home():
    return render_template('index.html')'''

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
        transid INT AUTO_INCREMENT PRIMARY KEY, 
        category VARCHAR(255), 
        amt DOUBLE(10,2), 
        item VARCHAR(255), 
        transaction_date DATE
    )
""")

# Function to insert transactions
while True:
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
    
    tup = tuple(l1)
    
    sql = "INSERT INTO transactiontable(category, amt, item, transaction_date) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, tup)
    mydb.commit()

    y = input("Add another transaction? (y/n): ")
    if y.lower() == 'n':
        break
# Route to handle form submission
'''@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form['category']
    item = request.form['item']
    amount = float(request.form['amount'])  # Convert string to float
    
    query = "INSERT INTO transactiontable (category, item, amt, transaction_date) VALUES (%s, %s, %s, %s)"
    values = (category, item, amount, date.today())  # Insert today's date
    
    mycursor = mydb.cursor()  # Ensure new cursor for each request
    mycursor.execute(query, values)
    mydb.commit()
    
    return redirect('/')
'''
# Function to get distinct categories
def categories_func():
    mycursor.execute("SELECT DISTINCT category FROM transactiontable")
    categories_data = mycursor.fetchall()
    categories_list = [item[0] for item in categories_data]  # Extract first element from each tuple
    return categories_list

# Fetch daily expenditure and reset if the date changes
def get_expenditure():
    current_date = date.today()
    mycursor.execute("SELECT amt, transaction_date FROM transactiontable")
    amt_data = mycursor.fetchall()

    daily_expenditure = sum(i[0] for i in amt_data if i[1] == current_date)  # Sum only today's transactions
    return daily_expenditure

# Main budget checking logic
def check_budget():
    global saved_up, emergency_fund
    daily_expenditure = get_expenditure()
    delta_1 = daily_budget - daily_expenditure
    
    # If the person spends less than the daily budget
    if delta_1 > 0:
        saved_up += delta_1  # Add the remaining budget to the savings
        print("Good job! You saved:", delta_1)
        print("Total saved up amount:", saved_up)
    else:
        print("WARNING! You have exceeded your daily budget.")
        delta_exceed = abs(delta_1)
        
        if delta_exceed > 2 * daily_budget:  # If exceeds more than twice the budget
            print(f"Warning: You have exceeded your daily budget by more than twice!")
            choice = input("Is this a one-time transaction? (y/n): ")
            
            if choice.lower() == 'y':
                print("Overflow warning will show until saved-up amount covers the excess.")
            else:
                # Handle emergency fund usage
                if delta_exceed <= emergency_fund:
                    use_emergency = input("Do you want to cover the difference with your emergency fund? (y/n): ")
                    if use_emergency.lower() == 'y':
                        emergency_fund -= delta_exceed
                        print(f"Covered by emergency fund. Remaining emergency fund: {emergency_fund}")
                    else:
                        print("Overflow warning remains.")
                else:
                    print("Your emergency fund is insufficient to cover this.")
                    empty_emergency = input("Do you want to empty the emergency fund? (y/n): ")
                    if empty_emergency.lower() == 'y':
                        delta_exceed -= emergency_fund
                        emergency_fund = 0
                        print(f"Emergency fund emptied. Remaining excess: {delta_exceed}")
                        choice = input("Is this a one-time transaction? (y/n): ")
                        if choice.lower() == 'n':
                            adjust_budget()  # Gradually increase the daily budget
                        else:
                            print("Overflow warning will show until saved-up amount covers the excess.")

# Function to gradually adjust the daily budget
def adjust_budget():
    global daily_budget
    dencrement = 0.05 * daily_budget  # Increase daily budget by 5%
    daily_budget -= dencrement
    print(f"Daily budget has been dencreased by 5%. New daily budget: {daily_budget}")

# Run budget check
check_budget()

'''if __name__ == '__main__':
    app.run(debug=True, port=5050)'''

def items_func():
    mycursor.execute("SELECT item, amt FROM transactiontable")
    items_data = mycursor.fetchall()
    items_list= [item[0] for item in items_data]
    return items_list

