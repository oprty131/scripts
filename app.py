from flask import Flask, render_template, request, jsonify
import threading
import time
import requests
import random
from urllib.parse import urlparse

app = Flask(__name__)

# Global variables for controlling sending process
sending = False
sent_requests = 0

# Function to extract item ID from TikTok URL
def extract_item_id(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    return path_segments[-1] if path_segments else None

def send_view_or_share(item_id, send_type, amount, proxies):
    global sending, sent_requests
    sent_requests = 0
    sending = True

    for _ in range(amount):
        if not sending:
            break
        # Randomly select a proxy
        proxy = random.choice(proxies)
        time.sleep(0.5)  # Simulate network delay

        # Simulate sending a view or share (replace with your actual logic)
        try:
            if send_type == 0:
                # Sending view
                print(f"Sending view for item {item_id} using proxy {proxy}")
                # Example request (mocked)
            else:
                # Sending share
                print(f"Sending share for item {item_id} using proxy {proxy}")
                # Example request (mocked)
            sent_requests += 1
        except Exception as e:
            print(f"Error sending: {e}")

    sending = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_sending():
    global sent_requests
    data = request.json
    url = data['url']
    send_type = data['sendType']
    amount = data['amount']
    proxies = data['proxies']

    item_id = extract_item_id(url)
    if not item_id:
        return jsonify({"status": "Invalid URL"}), 400

    # Start the sending process in a separate thread
    thread = threading.Thread(target=send_view_or_share, args=(item_id, send_type, amount, proxies))
    thread.start()

    return jsonify({"status": "sending started"})

@app.route('/stop', methods=['POST'])
def stop_sending():
    global sending
    sending = False
    return jsonify({"status": "sending stopped", "sent": sent_requests})

@app.route('/status', methods=['GET'])
def status():
    global sent_requests
    return jsonify({"sending": sending, "sent": sent_requests})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
