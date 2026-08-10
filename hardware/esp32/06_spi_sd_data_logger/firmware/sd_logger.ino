/*
 * ESP32-06 -- SPI SD Card Data Logger
 *
 * Samples a BME280 every second and appends CSV rows to an
 * auto-incrementing log file on a microSD card over SPI. A button
 * starts/stops each logging session.
 *
 * Libraries: Adafruit BME280 Library + Adafruit Unified Sensor
 * (SD and SPI ship with the ESP32 Arduino core).
 *
 * See ../README.md for the full pinout table.
 */

#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

const int SD_CS_PIN = 5;
const int BUTTON_PIN = 4;
const int STATUS_LED_PIN = 2;
const unsigned long SAMPLE_INTERVAL_MS = 1000;

Adafruit_BME280 bme;
File logFile;
bool logging = false;
bool sdReady = false;
bool bmeReady = false;

int lastButtonReading = HIGH;
int debouncedButtonState = HIGH;
unsigned long lastDebounceMs = 0;
unsigned long lastSampleMs = 0;
unsigned long lastBlinkMs = 0;
bool ledState = false;

String nextLogFilename() {
    for (int i = 0; i < 1000; i++) {
        char name[20];
        snprintf(name, sizeof(name), "/log_%03d.csv", i);
        if (!SD.exists(name)) {
            return String(name);
        }
    }
    return "/log_overflow.csv"; // fallback if we somehow fill 000-999
}

void startLogging() {
    String filename = nextLogFilename();
    logFile = SD.open(filename, FILE_WRITE);
    if (!logFile) {
        Serial.println("Failed to open log file");
        return;
    }
    logFile.println("millis,temp_c,humidity_pct,pressure_hpa");
    logging = true;
    Serial.print("Logging started: ");
    Serial.println(filename);
}

void stopLogging() {
    if (logFile) {
        logFile.flush();
        logFile.close();
    }
    logging = false;
    Serial.println("Logging stopped");
}

void handleButton() {
    int reading = digitalRead(BUTTON_PIN);
    if (reading != lastButtonReading) {
        lastDebounceMs = millis();
    }
    if (millis() - lastDebounceMs > 30) {
        if (reading != debouncedButtonState) {
            debouncedButtonState = reading;
            if (debouncedButtonState == LOW) { // press
                logging ? stopLogging() : startLogging();
            }
        }
    }
    lastButtonReading = reading;
}

void sampleAndLog() {
    float tempC = bme.readTemperature();
    float humidity = bme.readHumidity();
    float pressureHpa = bme.readPressure() / 100.0f;

    Serial.printf("T=%.1fC H=%.1f%% P=%.1fhPa\n", tempC, humidity, pressureHpa);

    if (logging && logFile) {
        logFile.printf("%lu,%.2f,%.2f,%.2f\n", millis(), tempC, humidity, pressureHpa);
        logFile.flush(); // periodic flush so a power loss only costs the last row, not the whole file
    }
}

void updateStatusLed() {
    if (!sdReady) {
        digitalWrite(STATUS_LED_PIN, HIGH); // solid = card error
        return;
    }
    if (logging) {
        if (millis() - lastBlinkMs > 250) {
            lastBlinkMs = millis();
            ledState = !ledState;
            digitalWrite(STATUS_LED_PIN, ledState);
        }
    } else {
        digitalWrite(STATUS_LED_PIN, LOW); // idle
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(STATUS_LED_PIN, OUTPUT);

    Wire.begin(21, 22);
    bmeReady = bme.begin(0x76);
    if (!bmeReady) {
        Serial.println("BME280 not found -- check wiring/I2C address");
    }

    sdReady = SD.begin(SD_CS_PIN);
    if (!sdReady) {
        Serial.println("SD card init failed -- check wiring/formatting (must be FAT32)");
    }

    Serial.println("sd_logger ready. Press the button to start/stop logging.");
}

void loop() {
    handleButton();
    updateStatusLed();

    if (bmeReady && sdReady && millis() - lastSampleMs > SAMPLE_INTERVAL_MS) {
        lastSampleMs = millis();
        sampleAndLog();
    }
}
