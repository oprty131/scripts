from flask import Flask, render_template, request
import requests

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
    except Exception as e:
        final_url = f"Error fetching URL: {str(e)}"

    # Return the expanded URL
    return render_template('index.html', final_url=final_url)

if __name__ == '__main__':
    app.run(debug=True)
