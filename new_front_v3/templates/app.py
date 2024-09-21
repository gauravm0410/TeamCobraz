from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Set a folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'textfile' not in request.files:
        return 'No file part'

    file = request.files['textfile']

    # If no file is selected
    if file.filename == '':
        return 'No selected file'

    # Save the file if it's a .txt file
    if file and file.filename.endswith('.txt'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Process the text file with a function
        result = process_file(filepath)

        # Return the result
        return result
    else:
        return 'Only .txt files are allowed.'

# Function to process the uploaded text file
def process_file(filepath):
    with open(filepath, 'r') as file:
        data = file.read()

    # Example processing: return the number of words in the text file
    word_count = len(data.split())

    # You can do more processing here with the data
    return f'The file has {word_count} words.'

if __name__ == '__main__':
    app.run(debug=True,port=5050)