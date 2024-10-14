from flask import Flask, render_template, request, jsonify
import threading
import time
import requests
import random
import os

app = Flask(__name__)

# Global variables for controlling sending process
sending = False
sent_requests = 0

def send_view_or_share(item_id, send_type, amount):
    global sending, sent_requests
    sent_requests = 0
    sending = True

    for _ in range(amount):
        if not sending:
            break
        # Simulate sending a view or share
        time.sleep(0.5)  # Simulate network delay
        sent_requests += 1

    sending = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_sending():
    global sent_requests
    data = request.json
    item_id = data['itemId']
    send_type = data['sendType']
    amount = data['amount']
    
    # Start the sending process in a separate thread
    thread = threading.Thread(target=send_view_or_share, args=(item_id, send_type, amount))
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
