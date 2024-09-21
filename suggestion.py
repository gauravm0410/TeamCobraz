import google.generativeai as genai
import json
from expense_explorer import *
import time

# Configure the Gemini API key
genai.configure(api_key="AIzaSyB3M56MfiQwFP3MbBMStmVW5j3-DQUIrvs")
model = genai.GenerativeModel('gemini-1.5-flash')

# Predefined categories
categories = list(categories_func())

# List of items to be categorized along with the amount spent on them
items = list(items_func())
# Dictionaries to store essential and non-essential categories with their total amounts
essentials = {}
non_essentials = {}

# Dictionary to keep track of categories, items, and their costs
category_items = {}

def categorizeItems():
    """
    Function to categorize items into specific categories. If a category does not exist, it is created.
    Items are assigned to their respective categories along with the amount spent on them.
    """
    chat = model.start_chat(history=[])
    tell_items = f"Categories these items as essential or non-essential: {str([items[0] for item in items])}. Return as dictionary"
    # for item, cost in items:
    #     # Ask the AI to categorize the item
    #     prompt = f"Categorize the item '{item}' into a proper category. Do not use bold text and do not describe anything"
    #     time.sleep(2)
    #     # Send the prompt to the model
    #     response = chat.send_message(prompt, stream=True)

    #     # Collect the full response from the stream
    #     output_text = ""
    #     for chunk in response:
    #         if hasattr(chunk, 'text') and chunk.text:
    #             output_text += chunk.text.lower()

    #     # Extract the category from the AI response
    #     category = output_text.strip()

    #     # If the category doesn't exist, add it to the categories list
    #     if category and category not in categories:
    #         categories.append(category)

    #     # Assign the item and its cost to its category in category_items dictionary
    #     if category not in category_items:
    #         category_items[category] = {}
    #     category_items[category][item] = cost
    response = chat.send_message(tell_items, stream=True)
    print(response)

    print("Categorized Items into Categories with Costs as a python dictionary: ", category_items)

categorizeItems()
print(category_items.keys())

def essentialAndNonEssential():
    """
    Function to classify which categories (that have items) are essential and non essential using AI.
    It returns two dictionary where each key is an essential category and non essential category, and each value is a 
    dictionary of items and costs.
    """
    chat = model.start_chat(history=[])
    
    # Initialize a dictionary to store essential categories
    essential_categories = {}

    prompt = f"Categorize the all item '{category_items}' into a essentials and non essentials category return as a json file without markdown and keys should be 'essentials' and 'non-essentials'"

    # Send the prompt to the model and collect the full response
    response = chat.send_message(prompt, stream=True)

    output_text = ""
    for chunk in response:
        if hasattr(chunk, 'text') and chunk.text:
            output_text += chunk.text.lower()
    
    output_text = output_text.replace("'", '"')
    output_text = output_text.replace("```json", '')
    output_text = output_text.replace("```", '')
    # Parse the JSON string into a Python dictionary
    data = json.loads(output_text)

    # Extract the essentials and non-essentials dictionaries
    global essentials
    global non_essentials
    essentials = data.get("essentials", {})
    non_essentials = data["non-essentials"]

    # Print the results
    print("Essentials:", essentials)
    print("Non-Essentials:", non_essentials)
        

essentialAndNonEssential()

essentials_sum = 0
non_essentials_sum = 0

# def sumEssential():
#     global essentials_sum
#     # Iterate through the categories and their items
#     for category, items in essentials.items():
#         for item, cost in items.items():
#             essentials_sum += cost

#     # Output the total sum of essential expenses
#     print("Total Essential Expenses:", essentials_sum)
# sumEssential()

# def sumNonEssential():
#     global non_essentials_sum
#     # Iterate through the categories and their items
#     for category, items in non_essentials.items():
#         for item, cost in items.items():
#             non_essentials_sum += cost

#     # Output the total sum of essential expenses
#     print("Total Non Essential Expenses:", non_essentials_sum)


# sumNonEssential()

# def smartSuggestions():
#     print(f"non essentials: {non_essentials}")
#     chat = model.start_chat(history=[])
#     prompt = f"analyse {items, for category, items in non_essentials.items} and tell where exactly and how much expenses i can cut down"
#     # Send the prompt to the model
#     response = chat.send_message(prompt, stream=True)

#     # Collect the full response from the stream
#     output_text = ""
#     for chunk in response:
#         if hasattr(chunk, 'text') and chunk.text:
#             output_text += chunk.text.lower()
#     print(output_text)

# smartSuggestions()


def smartSuggestions(non_essentials):
    """
    Function to provide smart saving suggestions based on the non-essential expenses.
    Suggests a 20% cut on each non-essential item and calculates the total monthly saving.
    """
    # Define the percentage cut for non-essential expenses (e.g., 20%)
    cut_percentage = 0.20
    
    # Initialize total monthly savings
    total_monthly_savings = 0
    
    # Dictionary to hold suggestions
    suggestions = {}

    # Iterate through each category and its items in non_essentials
    for category, items in non_essentials.items():
        suggestions[category] = {}
        for item, cost in items.items():
            # Calculate the amount to cut down for this item
            cut_amount = cost * cut_percentage
            
            # Add the cut suggestion to the dictionary
            suggestions[category][item] = round(cut_amount, 2)
            
            # Add to total monthly savings
            total_monthly_savings += cut_amount

    # Print the suggestions for each category and item
    for category, items in suggestions.items():
        print(f"Category: {category}")
        for item, cut_amount in items.items():
            print(f"  - You can cut down {item} by: ₹{cut_amount}")
    
    # Print the total monthly saving
    print(f"\nNet monthly savings if you cut down: ₹{round(total_monthly_savings, 2)}\n")
    
    return suggestions, total_monthly_savings

# Test the function
smartSuggestions(non_essentials)