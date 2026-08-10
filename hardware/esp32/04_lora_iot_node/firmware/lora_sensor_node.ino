/*
 * ESP32-04 -- LoRa IoT Sensor Node firmware
 *
 * Wakes on a timer, powers up the switched sensor rail (3V3_SENSORS via
 * the TPS22918 load switch), reads BME280 + BH1750 over I2C, transmits a
 * compact payload over LoRa (SPI), then powers the sensor rail back down
 * and deep-sleeps. This power sequencing is the whole point of this
 * board -- see ../README.md for the two-power-domain design.
 *
 * Libraries: "Adafruit BME280 Library" + "Adafruit Unified Sensor",
 * "BH1750" (claws81/Christopher Laws), "LoRa" (sandeepmistry/arduino-LoRa).
 *
 * Pin mapping (see ../README.md section 1):
 *   LoRa (SPI): SCK=18 MOSI=23 MISO=19 NSS=5  RST=14 DIO0=26
 *   Sensors (I2C): SDA=21 SCL=22 (BME280 addr 0x76, BH1750 addr 0x23)
 *   GPIO25 -> TPS22918 EN (switched 3V3_SENSORS rail)
 *   GPIO33 -> SW1 wake button (RTC-capable)
 *   GPIO2  -> D1 status LED
 */

#include <SPI.h>
#include <Wire.h>
#include <LoRa.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <BH1750.h>

const int LORA_SS = 5, LORA_RST = 14, LORA_DIO0 = 26;
const long LORA_FREQUENCY = 915E6; // set to your region's ISM band (868E6 in EU, etc.)

const int SENSOR_RAIL_EN_PIN = 25;
const int WAKE_BUTTON_PIN = 33;
const int STATUS_LED_PIN = 2;
const uint64_t SLEEP_DURATION_US = 5ULL * 60ULL * 1000000ULL; // 5 minutes between reports

Adafruit_BME280 bme;
BH1750 lightMeter;

struct SensorPayload {
    float temperatureC;
    float humidityPct;
    float pressureHpa;
    float luxLevel;
    float batteryVoltage;
};

float readBatteryVoltage() {
    // Placeholder -- wire an ADC-capable pin through a divider off the
    // battery rail if you want real battery telemetry; not in the base BOM.
    return analogRead(34) / 4095.0f * 3.3f * 2.0f;
}

bool readSensors(SensorPayload &payload) {
    if (!bme.begin(0x76)) return false;
    payload.temperatureC = bme.readTemperature();
    payload.humidityPct = bme.readHumidity();
    payload.pressureHpa = bme.readPressure() / 100.0f;

    lightMeter.begin();
    payload.luxLevel = lightMeter.readLightLevel();
    payload.batteryVoltage = readBatteryVoltage();
    return true;
}

void transmitPayload(const SensorPayload &payload) {
    LoRa.beginPacket();
    LoRa.print("T=");  LoRa.print(payload.temperatureC, 1);
    LoRa.print(",H="); LoRa.print(payload.humidityPct, 1);
    LoRa.print(",P="); LoRa.print(payload.pressureHpa, 1);
    LoRa.print(",L="); LoRa.print(payload.luxLevel, 1);
    LoRa.print(",V="); LoRa.print(payload.batteryVoltage, 2);
    LoRa.endPacket();
}

void goToSleep() {
    esp_sleep_enable_timer_wakeup(SLEEP_DURATION_US);
    esp_sleep_enable_ext0_wakeup((gpio_num_t)WAKE_BUTTON_PIN, 0);
    esp_deep_sleep_start();
}

void setup() {
    Serial.begin(115200);
    pinMode(SENSOR_RAIL_EN_PIN, OUTPUT);
    pinMode(WAKE_BUTTON_PIN, INPUT_PULLUP);
    pinMode(STATUS_LED_PIN, OUTPUT);

    digitalWrite(SENSOR_RAIL_EN_PIN, HIGH); // power up 3V3_SENSORS
    delay(20); // let sensors' regulators settle before talking to them
    Wire.begin(21, 22);

    LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
    bool radioReady = LoRa.begin(LORA_FREQUENCY);

    SensorPayload payload{};
    bool sensorsReady = readSensors(payload);

    if (radioReady && sensorsReady) {
        digitalWrite(STATUS_LED_PIN, HIGH);
        transmitPayload(payload);
        Serial.printf("TX: T=%.1f H=%.1f P=%.1f L=%.1f V=%.2f\n",
                       payload.temperatureC, payload.humidityPct,
                       payload.pressureHpa, payload.luxLevel, payload.batteryVoltage);
        digitalWrite(STATUS_LED_PIN, LOW);
    } else {
        Serial.println(radioReady ? "Sensor read failed" : "LoRa radio init failed");
    }

    digitalWrite(SENSOR_RAIL_EN_PIN, LOW); // power down sensors before sleeping
    goToSleep();
}

void loop() {
    // Never reached -- setup() ends in deep sleep.
}
