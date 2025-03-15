import requests
import random
import time
import json

SERVER_URL = "http://192.168.42.252:3005/data"

# Thermostat temperature ranges
BASE_TEMP = 25.0
NORMAL_TEMP_RANGE = (18.0, 30.0)

# Attack parameters
ATTACK_DURATION = 300  # Duration of attack in seconds (e.g., 5 minutes)
ATTACK_FREQUENCY = 0.5  # Time interval between each attack packet (e.g., 0.5 seconds)

def generate_temperature_data(is_attack=False):
    """Generate realistic temperature data for thermostat"""
    noise = random.uniform(-2.0, 2.0)  # Small random variation for realism
    temperature = BASE_TEMP + noise

    if is_attack:
        anomaly_type = random.choice(["spike", "drop", "erratic"])
        if anomaly_type == "spike":
            temperature += random.uniform(10, 15)  # Sharp increase
        elif anomaly_type == "drop":
            temperature -= random.uniform(10, 15)  # Sharp decrease
        elif anomaly_type == "erratic":
            temperature += random.uniform(-15, 15)  # Random fluctuations

    return round(temperature, 2)

def send_data(is_attack=False):
    """Send data to the server"""
    temperature = generate_temperature_data(is_attack)
    data_type = "ddos_attack" if is_attack else "normal"

    payload = {
        "device": "ATTACK_SIMULATOR",
        "temperature": temperature,
        "type": data_type
    }

    try:
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ Sent: {payload}")
        else:
            print(f"❌ Failed to send data. HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_simulation():
    """Control flow for attack and normal data simulation"""
    print("🚨 Attack Simulation Started...")

    start_time = time.time()

    while time.time() - start_time < ATTACK_DURATION:
        # Alternate between attack and normal data
        if random.random() < 0.5:  # 50% chance of attack or normal
            send_data(is_attack=True)   # Send attack data
        else:
            send_data(is_attack=False)  # Send normal data

        time.sleep(ATTACK_FREQUENCY)

    print("✅ Attack Simulation Finished!")

if __name__ == "__main__":
    run_simulation()
