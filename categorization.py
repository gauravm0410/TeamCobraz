# in this the categories will come from arnav's database i will create a function to append user defined categories into the categories list 
# and we will also have pre defined categories already in the list
# THOROUGH TESTING IS NEEDED IN THIS CATEGORIZATION check all weird kind of inputs


import google.generativeai as genai
import os
from expense_explorer import *

# Configure the Gemini API key
genai.configure(api_key="AIzaSyCjjpCygGd_nECRyFmEwUzjpT70ZLywV68")
model = genai.GenerativeModel('gemini-pro')

categories = categories_func()

essential = []
non_essential = []

def essentialCategory():
    chat = model.start_chat(history=[])
    # Format the list into a string prompt
    prompt1 = "Give only essential expenses and give output without any special characters and unnecessary information: " + ', '.join(categories)

    # Send the prompt to the model
    response1 = chat.send_message(prompt1, stream=True)
    
    for chunk in response1:
        if hasattr(chunk, 'text') and chunk.text:
            output_text = chunk.text.lower()

    # Split response into lines
        lines = output_text.split("\n")
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            essential.append(line)

    return essential


def nonEssentialCategory():
    chat = model.start_chat(history=[])
    # Format the list into a string prompt
    prompt = "Give only non-essential expenses and give output without any special characters and unnecessary information: " + ', '.join(categories)
 
    # Send the prompt to the model
    response = chat.send_message(prompt, stream=True)
    
    for chunk in response:
        if hasattr(chunk, 'text') and chunk.text:
            output_text = chunk.text.lower()
        
    # Split response into lines
        lines = output_text.split("\n")
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            non_essential.append(line)

    return non_essential

print(f"essential category : {essentialCategory()}")
print(f"non essential category : {nonEssentialCategory()}")