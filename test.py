import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyCjjpCygGd_nECRyFmEwUzjpT70ZLywV68")
model = genai.GenerativeModel('gemini-pro')

# Predefined categories
categories = ["rent", "food", "shopping", "netflix"]

# List of items to be categorized
items = ["basketball", "rent", "pizza", "netflix"]

# Sets to avoid duplicates
essential = set()
non_essential = set()

# Dictionary to keep track of which items belong to which categories
category_items = {}

def categorizeItems():
    """
    Function to categorize items into specific categories. If a category does not exist, it is created.
    Items are assigned to their respective categories.
    """
    chat = model.start_chat(history=[])
    
    for item in items:
        # Ask the AI to categorize the item
        prompt = f"Categorize the item '{item}' into a proper category."
        
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

        # Assign the item to its category in category_items dictionary
        if category not in category_items:
            category_items[category] = []
        category_items[category].append(item)

    print("Categorized Items into Categories:", category_items)

def essentialCategory():
    """
    Function to classify which categories (that have items) are essential using AI.
    """
    chat = model.start_chat(history=[])
    
    # Filter categories that have assigned items
    valid_categories = [cat for cat in category_items if category_items[cat]]

    if valid_categories:
        prompt1 = "Give only essential expenses and give output without any special characters and unnecessary information: " + ', '.join(valid_categories)

        # Send the prompt to the model and collect the full response
        response1 = chat.send_message(prompt1, stream=True)

        output_text = ""
        for chunk in response1:
            if hasattr(chunk, 'text') and chunk.text:
                output_text += chunk.text.lower()

        # Process the response and split into essential items
        lines = output_text.split("\n")
        for line in lines:
            line = line.strip()
            if line:
                essential.add(line)

    return list(essential)

def nonEssentialCategory():
    """
    Function to classify which categories (that have items) are non-essential using AI.
    """
    chat = model.start_chat(history=[])
    
    # Filter categories that have assigned items
    valid_categories = [cat for cat in category_items if category_items[cat]]

    if valid_categories:
        prompt = "Give only non-essential expenses and give output without any special characters and unnecessary information: " + ', '.join(valid_categories)

        # Send the prompt to the model and collect the full response
        response = chat.send_message(prompt, stream=True)

        output_text = ""
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                output_text += chunk.text.lower()

        # Process the response and split into non-essential items
        lines = output_text.split("\n")
        for line in lines:
            line = line.strip()
            if line:
                non_essential.add(line)

    return list(non_essential)

# Function to test item categorization and then run essential/non-essential categorization
def runProgram():
    print("Original Categories:", categories)
    print("Items to categorize:", items)

    # Step 1: Categorize items into categories
    categorizeItems()

    # Step 2: Classify the categories (with assigned items) into essential and non-essential
    print("Essential Categories:", essentialCategory())
    print("Non-Essential Categories:", nonEssentialCategory())

# Test the program
runProgram()

def smartSuggestions(ess_exp : float, non_ess_exp : float , daily_budget : float):
    total_daily_exp = ess_exp + non_ess_exp
    chat = model.start_chat(history=[])
    if total_daily_exp > daily_budget:
        prompt = f"analyse {non_essential} tell me how  much i can cut down in each category and tell net savings "
        response = chat.send_message(prompt, stream=True)
        output_text = ""
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                output_text += chunk.text.lower()
                print(output_text)

smartSuggestions(ess_exp = 100, non_ess_exp = 110, daily_budget = 200)
