# Initialize empty lists for storing different parts of the transaction data
amounts = []
dates = []
transaction_ids = []  # Changed this to store transaction IDs only
categories = []
items = []

# File path for the transaction file
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

# Now you have:
# amounts: list of integers representing transaction amounts
# dates: list of strings representing transaction dates
# transaction_ids: list of strings representing transaction IDs
# categories: list of strings representing payment categories
# items: list of strings representing the items bought
print(amounts)
print(dates)
print(transaction_ids)
print(categories)
print(items)