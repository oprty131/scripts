from flask import Flask, render_template, request, redirect
import requests
import pyperclip  # To copy the URL to the clipboard

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expand', methods=['POST'])
def expand_url():
    original_url = request.form['url']
    
    try:
        # Fetch the final redirected URL
        response = requests.get(original_url, allow_redirects=True)
        final_url = response.url
        
        # Copy the final URL to the clipboard
        pyperclip.copy(final_url)
        
        # Redirect back to the home page, showing a success message
        return render_template('index.html', final_url=final_url)
        
    except Exception as e:
        # Return an error if there's a problem fetching the URL
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
