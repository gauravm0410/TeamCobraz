import mysql.connector
from datetime import date
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Arn@Ana@2897"
)
monthly_budget=float(input("Enter your monthly budge: "))
daily_budget=monthly_budget/30
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS expenseexplorer")
mycursor.execute("USE expenseexplorer")
mycursor.execute("CREATE TABLE IF NOT EXISTS transactiontable(transid INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255), amt DOUBLE(10,2), item VARCHAR(255), trans_date DATE)")
tup=()
l1=[]
while True:
    cat=input("Enter category of expenditure: ")
    amount=float(input("Enter cost of purchase: "))
    item=input("Enter item name: ")
    current_date=date.today()
    l1.append(cat)
    l1.append(amount)
    l1.append(item)
    l1.append(current_date)
    tup=tuple(l1)
    sql="INSERT INTO transactiontable(category, amt, item, transdate) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, tup)
    mydb.commit()
    y=input("Add another transaction?(y/n): ")
    if y=='n':
        break
    

def categories_func():
  mycursor.execute("SELECT DISTINCT category FROM transactiontable")
  categories_data=mycursor.fetchall()
  categories_list=list(categories_data)
  return categories_list



mycursor.execute("SELECT amt FROM transactiontable")
amt_data=mycursor.fetchall()
amt_list=list(amt_data)
daily_expenditure, monthly_expenditure=0,0
for i in amt_list:
    daily_expenditure+=i
monthly_expenditure+=daily_expenditure
delta_1=daily_budget-daily_expenditure
if delta_1<0:
    print("WARNING!!")
