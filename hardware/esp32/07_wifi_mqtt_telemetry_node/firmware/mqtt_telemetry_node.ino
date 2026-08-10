/*
 * ESP32-07 -- WiFi/MQTT Telemetry Node
 *
 * Publishes a JSON light-level reading to MQTT every 5s, subscribes to a
 * command topic to remotely drive a relay, and handles WiFi/MQTT
 * reconnection so it survives router hiccups instead of just going silent.
 *
 * Libraries: PubSubClient (Nick O'Leary), ArduinoJson (Benoit Blanchon).
 *
 * See ../README.md for the full pinout table and broker setup.
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// --- Config: edit before flashing ---
const char *WIFI_SSID = "your-ssid";
const char *WIFI_PASSWORD = "your-password";
const char *MQTT_BROKER = "test.mosquitto.org";
const int MQTT_PORT = 1883;
const char *MQTT_CLIENT_ID = "esp32-telemetry-node";
const char *TOPIC_DATA = "esp32/telemetry_node/data";
const char *TOPIC_CMD = "esp32/telemetry_node/cmd";
// --- End config ---

const int LDR_PIN = 34;
const int RELAY_PIN = 26;
const int STATUS_LED_PIN = 2;
const unsigned long PUBLISH_INTERVAL_MS = 5000;

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
unsigned long lastPublishMs = 0;
unsigned long lastLedBlinkMs = 0;
bool relayState = false;

void mqttCallback(char *topic, byte *payload, unsigned int length) {
    String message;
    for (unsigned int i = 0; i < length; i++) message += (char)payload[i];

    if (String(topic) == TOPIC_CMD) {
        if (message == "ON") {
            relayState = true;
        } else if (message == "OFF") {
            relayState = false;
        }
        digitalWrite(RELAY_PIN, relayState ? HIGH : LOW);
        Serial.printf("Command received: %s -> relay %s\n", message.c_str(), relayState ? "ON" : "OFF");
    }
}

void ensureWifiConnected() {
    if (WiFi.status() == WL_CONNECTED) return;

    Serial.println("WiFi disconnected, (re)connecting...");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    unsigned long start = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
        delay(250);
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.print("WiFi connected, IP=");
        Serial.println(WiFi.localIP());
    }
}

void ensureMqttConnected() {
    if (mqtt.connected()) return;

    Serial.print("Connecting to MQTT broker...");
    if (mqtt.connect(MQTT_CLIENT_ID)) {
        Serial.println(" connected");
        mqtt.subscribe(TOPIC_CMD); // subscriptions don't survive a disconnect -- must re-subscribe here
    } else {
        Serial.printf(" failed, rc=%d\n", mqtt.state());
    }
}

void publishTelemetry() {
    int lightRaw = analogRead(LDR_PIN);

    StaticJsonDocument<128> doc;
    doc["light_raw"] = lightRaw;
    doc["relay"] = relayState;
    doc["uptime_s"] = millis() / 1000;

    char payload[128];
    size_t len = serializeJson(doc, payload);
    mqtt.publish(TOPIC_DATA, (const uint8_t *)payload, len);

    Serial.print("Published: ");
    Serial.println(payload);
}

void updateStatusLed() {
    bool wifiOk = (WiFi.status() == WL_CONNECTED);
    bool mqttOk = mqtt.connected();

    if (wifiOk && mqttOk) {
        digitalWrite(STATUS_LED_PIN, HIGH); // solid = fully connected
    } else if (wifiOk) {
        if (millis() - lastLedBlinkMs > 500) { // blinking = WiFi ok, MQTT not yet
            lastLedBlinkMs = millis();
            digitalWrite(STATUS_LED_PIN, !digitalRead(STATUS_LED_PIN));
        }
    } else {
        digitalWrite(STATUS_LED_PIN, LOW); // off = no WiFi
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(STATUS_LED_PIN, OUTPUT);

    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    mqtt.setCallback(mqttCallback);

    ensureWifiConnected();
}

void loop() {
    ensureWifiConnected();
    if (WiFi.status() == WL_CONNECTED) {
        ensureMqttConnected();
        mqtt.loop(); // must be called regularly to process incoming messages/keepalive
    }

    updateStatusLed();

    if (mqtt.connected() && millis() - lastPublishMs > PUBLISH_INTERVAL_MS) {
        lastPublishMs = millis();
        publishTelemetry();
    }
}
