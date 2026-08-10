/*
 * ESP32-08 -- BLE Sensor Beacon
 *
 * BLE GATT server exposing:
 *   - a notify characteristic streaming a potentiometer reading whenever
 *     it changes by more than a threshold
 *   - a read/write characteristic that remotely toggles the onboard LED
 *
 * Uses the ESP32 Arduino core's bundled BLE library (BLEDevice/BLEServer).
 * See ../README.md for the full pinout table and how to test with nRF
 * Connect (no custom app needed).
 */

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID        "4a981234-0000-1000-8000-00805f9b34fb"
#define SENSOR_CHAR_UUID     "4a981234-0000-1000-8000-000000000001"
#define LED_CHAR_UUID        "4a981234-0000-1000-8000-000000000002"

const int SENSOR_PIN = 34;
const int LED_PIN = 2;
const int CHANGE_THRESHOLD = 20; // out of 4095 -- avoids spamming notifications on ADC noise
const unsigned long POLL_INTERVAL_MS = 200;

BLEServer *bleServer = nullptr;
BLECharacteristic *sensorCharacteristic = nullptr;
BLECharacteristic *ledCharacteristic = nullptr;
bool deviceConnected = false;
int lastNotifiedValue = -1000;
unsigned long lastPollMs = 0;

class ServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer *server) override {
        deviceConnected = true;
        Serial.println("BLE client connected");
    }
    void onDisconnect(BLEServer *server) override {
        deviceConnected = false;
        Serial.println("BLE client disconnected, resuming advertising");
        server->getAdvertising()->start(); // BLE stops advertising on connect; restart it after disconnect
    }
};

class LedCharacteristicCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *characteristic) override {
        std::string value = characteristic->getValue();
        if (value.length() > 0) {
            bool ledOn = (value[0] != 0);
            digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
            Serial.printf("LED set to %s via BLE\n", ledOn ? "ON" : "OFF");
        }
    }
};

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);

    BLEDevice::init("ESP32-SensorBeacon");
    bleServer = BLEDevice::createServer();
    bleServer->setCallbacks(new ServerCallbacks());

    BLEService *service = bleServer->createService(SERVICE_UUID);

    sensorCharacteristic = service->createCharacteristic(
        SENSOR_CHAR_UUID, BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
    sensorCharacteristic->addDescriptor(new BLE2902()); // required for notify() to actually reach the client

    ledCharacteristic = service->createCharacteristic(
        LED_CHAR_UUID, BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
    ledCharacteristic->setCallbacks(new LedCharacteristicCallbacks());
    ledCharacteristic->setValue("0");

    service->start();

    BLEAdvertising *advertising = BLEDevice::getAdvertising();
    advertising->addServiceUUID(SERVICE_UUID);
    advertising->setScanResponse(true);
    BLEDevice::startAdvertising();

    Serial.println("BLE advertising as ESP32-SensorBeacon");
}

void loop() {
    if (millis() - lastPollMs < POLL_INTERVAL_MS) return;
    lastPollMs = millis();

    int value = analogRead(SENSOR_PIN);

    if (deviceConnected && abs(value - lastNotifiedValue) > CHANGE_THRESHOLD) {
        lastNotifiedValue = value;
        char payload[8];
        snprintf(payload, sizeof(payload), "%d", value);
        sensorCharacteristic->setValue(payload);
        sensorCharacteristic->notify();
        Serial.printf("Notified sensor value: %d\n", value);
    }
}
