import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Arn@Ana@2897"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS expenseexplorer")
mycursor.execute("USE expenseexplorer")
mycursor.execute("CREATE TABLE IF NOT EXISTS transactiontable(transid INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255), amt DOUBLE(10,2), item VARCHAR(255))")
#list=[]
tup=()
l1=[]
while True:
    cat=input("Enter category of expenditure: ")
    amount=float(input("Enter cost of purchase: "))
    item=input("Enter item name: ")
    l1.append(cat)
    l1.append(amount)
    l1.append(item)
    tup=tuple(l1)
    sql="INSERT INTO transactiontable(category, amt, item) VALUES (%s, %s, %s)"
    mycursor.execute(sql, tup)
    mydb.commit()
    y=input("Add another transaction?(y/n): ")
    if y=='n':
        break
mycursor.execute("SELECT * from transactiontable")
data=mycursor.fetchall()
data2=list(data)