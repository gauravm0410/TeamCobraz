import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyCjjpCygGd_nECRyFmEwUzjpT70ZLywV68")
model = genai.GenerativeModel('gemini-1.5-flash')

# Predefined categories
categories = ["rent", "food", "shopping", "netflix"]

# List of items to be categorized along with the amount spent on them
items = [("basketball", 50), ("rent", 1200), ("pizza", 20), ("netflix", 15)]

# Dictionaries to store essential and non-essential categories with their total amounts
essential = {}
non_essential = {}

# Dictionary to keep track of categories, items, and their costs
category_items = {}

def categorizeItems():
    """
    Function to categorize items into specific categories. If a category does not exist, it is created.
    Items are assigned to their respective categories along with the amount spent on them.
    """
    chat = model.start_chat(history=[])
    
    for item, cost in items:
        # Ask the AI to categorize the item
        prompt = f"Categorize the item '{item}' into a proper category.do not use bold text and do not describe anything"
        
        # Send the prompt to the model
        response = chat.send_message(prompt, stream=True)

        # Collect the full response from the stream
        output_text = ""
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                output_text += chunk.text.lower()

        # Extract the category from the AI response
        category = output_text.strip()

        # If the category doesn't exist, add it to the categories list
        if category and category not in categories:
            categories.append(category)

        # Assign the item and its cost to its category in category_items dictionary
        if category not in category_items:
            category_items[category] = {}
        category_items[category][item] = cost


    print("Categorized Items into Categories with Costs as a python dictionary: ", category_items)

categorizeItems()

def essentialCategory():
    """
    Function to classify which categories (that have items) are essential using AI.
    It returns a dictionary where each key is an essential category, and each value is a 
    dictionary of items and costs.
    """
    chat = model.start_chat(history=[])
    
    # Initialize a dictionary to store essential categories
    essential_categories = {}

    prompt = "Give only essential expenses and give output without any special characters and unnecessary information: " + ', '.join(category_items)

    # Send the prompt to the model and collect the full response
    response = chat.send_message(prompt, stream=True)

    output_text = ""
    for chunk in response:
        if hasattr(chunk, 'text') and chunk.text:
            output_text += chunk.text.lower()

    # Process the response and split into essential items
    lines = output_text.split("\n")
    for line in lines:
        line = line.strip()
        if line and line in category_items:
            # Add the category and its items to the essential_categories dictionary
            essential_categories[line] = category_items[line]  # Assign the entire dictionary of items and costs
    print(essential_categories)
    return essential_categories

essentialCategory()

def createEssentialsDictionary():
    """
    Function to create an essentials dictionary.
    Each key is the category name, and each value is a dictionary of items and their respective costs.
    """
    essentials_dict = {}

    # Get the essential categories using the existing essentialCategory() function
    essential_categories = essentialCategory()  # This function should return a dictionary of essentials

    for category, items in essential_categories.items():
        # Create a new entry in the essentials_dict for each category
        essentials_dict[category] = items  # 'items' is already a dictionary of item names and costs
    print(f"essential dictionary is : {essentials_dict}")
    return essentials_dict

createEssentialsDictionary()
