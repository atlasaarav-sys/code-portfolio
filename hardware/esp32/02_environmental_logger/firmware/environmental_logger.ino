/*
 * ESP32-02 -- Environmental Logger firmware
 *
 * Reads temperature/humidity/pressure from a BME280 over I2C, shows live
 * readings on an SSD1306 OLED (same I2C bus), and deep-sleeps between
 * reads to stretch battery life -- this is the piece that actually needs
 * firmware discipline on a battery board (see ../README.md for the power
 * architecture: LiPo + charger + always-on 3V3 rail).
 *
 * Libraries (Arduino Library Manager):
 *   "Adafruit BME280 Library" + "Adafruit Unified Sensor"
 *   "Adafruit SSD1306" + "Adafruit GFX Library"
 *
 * Pin mapping (see ../README.md section 1):
 *   GPIO21 -> SDA (shared bus: BME280 + OLED)
 *   GPIO22 -> SCL (shared bus: BME280 + OLED)
 *   GPIO2  -> D2 status LED
 *   GPIO4  -> SW4 wake/mode button (RTC-capable on most WROOM-32 variants)
 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SEALEVELPRESSURE_HPA (1013.25)
const int STATUS_LED_PIN = 2;
const int WAKE_BUTTON_PIN = 4;
const uint64_t SLEEP_DURATION_US = 60ULL * 1000000ULL; // read every 60s

Adafruit_BME280 bme;
Adafruit_SSD1306 display(128, 64, &Wire, -1);

bool readSensor(float &tempC, float &humidity, float &pressureHpa) {
    if (!bme.begin(0x76)) {
        return false;
    }
    tempC = bme.readTemperature();
    humidity = bme.readHumidity();
    pressureHpa = bme.readPressure() / 100.0F;
    return true;
}

void showReading(float tempC, float humidity, float pressureHpa) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print("Temp: "); display.print(tempC, 1); display.println(" C");
    display.print("Hum:  "); display.print(humidity, 1); display.println(" %");
    display.print("Pres: "); display.print(pressureHpa, 1); display.println(" hPa");
    display.display();
}

void goToSleep() {
    display.ssd1306_command(SSD1306_DISPLAYOFF); // save power before sleeping
    esp_sleep_enable_timer_wakeup(SLEEP_DURATION_US);
    esp_sleep_enable_ext0_wakeup((gpio_num_t)WAKE_BUTTON_PIN, 0); // wake early on button press
    esp_deep_sleep_start();
}

void setup() {
    Serial.begin(115200);
    pinMode(STATUS_LED_PIN, OUTPUT);
    pinMode(WAKE_BUTTON_PIN, INPUT_PULLUP);
    digitalWrite(STATUS_LED_PIN, HIGH);

    Wire.begin(21, 22);

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("SSD1306 init failed");
    }

    float tempC, humidity, pressureHpa;
    if (readSensor(tempC, humidity, pressureHpa)) {
        Serial.printf("T=%.1fC H=%.1f%% P=%.1fhPa\n", tempC, humidity, pressureHpa);
        showReading(tempC, humidity, pressureHpa);
    } else {
        Serial.println("BME280 not found -- check wiring/I2C address");
        display.clearDisplay();
        display.setCursor(0, 0);
        display.println("BME280 error");
        display.display();
    }

    delay(3000); // let the reading stay on screen briefly before sleeping
    digitalWrite(STATUS_LED_PIN, LOW);
    goToSleep();
}

void loop() {
    // Never reached -- setup() ends in deep sleep, and reset re-runs setup().
}
