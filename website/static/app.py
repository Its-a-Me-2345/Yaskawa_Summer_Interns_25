from flask import Flask, render_template, request
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Path for the CSV log file
LOG_FILE = 'gesture_log.csv'

# Create CSV with headers if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Command'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/voice')
def voice():
    return render_template('voice.html')

@app.route('/gesture')
def gesture():
    return render_template('gesture.html')

@app.route('/log-gesture', methods=['POST'])
def log_gesture():
    data = request.get_json()
    gesture = data.get('gesture')
    timestamp = data.get('timestamp')

    # Use current time if not provided
    if not timestamp:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Map gesture names to robot axis-direction commands
    gesture_map = {
        'victory': 'X+',
        'yo': 'X-',
        'thumbs_up': 'Z+',
        'thumbs_down': 'Z-',
    }

    command = gesture_map.get(gesture, 'UNKNOWN')

    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, command])

    return 'Gesture logged successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
