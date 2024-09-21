from collections import defaultdict

# Initialize a dictionary to store total expenditure per day
expenditure_per_day = defaultdict(int)

# File path for the transaction file
file_path = 'extended_transaction_details.txt'

# Open and read the transaction file
with open(file_path, 'r') as file:
    for line in file:
        # Split the line to get transaction details
        txn_id, amount, date, item, category = line.strip().split(', ')
        
        # Add the amount to the respective date's total expenditure
        expenditure_per_day[date] += int(amount)

# Now expenditure_per_day contains the total expenditure per date
for date, total in expenditure_per_day.items():
    print(f"Total expenditure on {date}: {total}")
