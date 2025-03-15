from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

# CSV File Path
DATASET_PATH = "smart_plug_dataset.csv"

# Initialize CSV File with Headers if it doesn't exist
if not os.path.exists(DATASET_PATH):
    with open(DATASET_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "device_id", "power_w", "voltage_v", "current_a", "label"])

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json

    device_id = data.get("device_id", "Unknown")
    power_w = float(data.get("power_w", 0.0))
    voltage_v = float(data.get("voltage_v", 0.0))
    current_a = float(data.get("current_a", 0.0))
    label = data.get("label", "normal")

    # Log received data
    print(f"📥 Data Received - Device: {device_id}, Power: {power_w}, Voltage: {voltage_v}, Current: {current_a}")

    # Write data to CSV file
    with open(DATASET_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            device_id,
            power_w,
            voltage_v,
            current_a,
            label
        ])

    return jsonify({"status": "success", "message": "Data logged successfully"}), 200

if __name__ == '__main__':
    print("🚀 Server running on port 3005")
    app.run(host='0.0.0.0', port=3006, debug=True)
