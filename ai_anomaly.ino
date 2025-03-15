#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "Recruitment";
const char* password = "none4142";

// Server URL
const char* serverURL = "http://192.168.200.84:3005/data";  // Replace with your server IP

// Smart Plug Device ID
const char* deviceId = "Device_ESP32";

// Simulated Sensor Readings (Replace with actual sensor readings)
float power_w = 45.0; // Start with a default "normal" power value
float voltage_v = 219.5;
float current_a = 0.205;

// Time between sending data (milliseconds)
const unsigned long interval = 3000;  // Send data every 3 seconds
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Simulate sensor readings (replace with actual sensor code)

    //Keep the value within range, with slight variance
    power_w = constrain(power_w + random(-3, 3), 35, 48); // Even more restriction and focus on lower power
    voltage_v = constrain(voltage_v + random(-0.5, 0.5), 219, 220);  // Small voltage fluctuations
    current_a = power_w / voltage_v;  // Calculate current from power and voltage

    // Prepare JSON payload
    StaticJsonDocument<256> doc;
    doc["device_id"] = deviceId;
    doc["power_w"] = power_w;
    doc["voltage_v"] = voltage_v;
    doc["current_a"] = current_a;

    String json;
    serializeJson(doc, json);

    // Send data to server
    sendData(json);
  }
}

void sendData(String jsonPayload) {
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(jsonPayload);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    if (httpResponseCode == 200) {
      String response = http.getString();
      Serial.println("Server response: " + response);

      // Parse the response JSON
      StaticJsonDocument<256> responseDoc;
      DeserializationError error = deserializeJson(responseDoc, response);

      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.c_str());
        return;
      }

      const char* status = responseDoc["status"];
      const char* action = responseDoc["action"];

      Serial.print("Status: ");
      Serial.println(status);
      Serial.print("Action: ");
      Serial.println(action);
    }
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}