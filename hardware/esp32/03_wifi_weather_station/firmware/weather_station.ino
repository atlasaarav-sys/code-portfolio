/*
 * ESP32-03 -- WiFi Weather Station firmware
 *
 * Joins WiFi, syncs time from NTP, keeps a DS3231 RTC as an offline
 * fallback, shows a live dashboard on an ILI9341 TFT, and appends a CSV
 * log line to a microSD card once a minute. TFT and SD share the SPI bus
 * (SCK/MOSI/MISO) with separate CS lines, as documented in ../README.md.
 *
 * Libraries: "Adafruit ILI9341", "Adafruit GFX Library", "RTClib", "SD"
 * (bundled with the ESP32 Arduino core).
 *
 * Pin mapping (see ../README.md section 1):
 *   TFT: SCK=18 MOSI=23 MISO=19 CS=5  DC=2  RST=4
 *   SD:  SCK=18 MOSI=23 MISO=19 CS=15 (shared bus, dedicated CS)
 *   RTC: SDA=21 SCL=22 (I2C)
 *   SW3=32 (mode), SW4=33 (next), D1=13 (status LED)
 */

#include <SPI.h>
#include <Wire.h>
#include <WiFi.h>
#include <time.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <RTClib.h>
#include <SD.h>

const char *WIFI_SSID = "your-ssid";
const char *WIFI_PASSWORD = "your-password";
const char *NTP_SERVER = "pool.ntp.org";

const int TFT_CS = 5, TFT_DC = 2, TFT_RST = 4;
const int SD_CS = 15;
const int MODE_BUTTON_PIN = 32, NEXT_BUTTON_PIN = 33, STATUS_LED_PIN = 13;
const unsigned long LOG_INTERVAL_MS = 60000;

Adafruit_ILI9341 tft(TFT_CS, TFT_DC, TFT_RST);
RTC_DS3231 rtc;
bool sdAvailable = false;
bool wifiConnected = false;
unsigned long lastLogMs = 0;

void connectWifi(unsigned long timeoutMs = 10000) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    unsigned long start = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - start < timeoutMs) {
        delay(250);
    }
    wifiConnected = (WiFi.status() == WL_CONNECTED);
    if (wifiConnected) {
        configTime(0, 0, NTP_SERVER); // UTC; adjust offset for local time if needed
    }
}

void syncRtcFromNtpIfPossible() {
    if (!wifiConnected) return;
    struct tm timeinfo;
    if (getLocalTime(&timeinfo, 5000)) {
        rtc.adjust(DateTime(timeinfo.tm_year + 1900, timeinfo.tm_mon + 1, timeinfo.tm_mday,
                             timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec));
        Serial.println("RTC synced from NTP");
    }
}

void drawDashboard(DateTime now) {
    tft.fillScreen(ILI9341_BLACK);
    tft.setTextColor(ILI9341_WHITE);
    tft.setTextSize(2);
    tft.setCursor(10, 10);
    tft.printf("%04d-%02d-%02d", now.year(), now.month(), now.day());
    tft.setCursor(10, 35);
    tft.printf("%02d:%02d:%02d", now.hour(), now.minute(), now.second());

    tft.setTextSize(1);
    tft.setCursor(10, 70);
    tft.print("WiFi: ");
    tft.print(wifiConnected ? "connected" : "offline (RTC fallback)");
    tft.setCursor(10, 85);
    tft.print("SD log: ");
    tft.print(sdAvailable ? "OK" : "not present");
}

void logToSd(DateTime now) {
    if (!sdAvailable) return;
    File f = SD.open("/weather_log.csv", FILE_APPEND);
    if (!f) return;
    f.printf("%04d-%02d-%02dT%02d:%02d:%02d\n", now.year(), now.month(), now.day(),
             now.hour(), now.minute(), now.second());
    f.close();
}

void setup() {
    Serial.begin(115200);
    pinMode(MODE_BUTTON_PIN, INPUT_PULLUP);
    pinMode(NEXT_BUTTON_PIN, INPUT_PULLUP);
    pinMode(STATUS_LED_PIN, OUTPUT);

    Wire.begin(21, 22);
    if (!rtc.begin()) {
        Serial.println("DS3231 not found -- check I2C wiring");
    }

    tft.begin();
    tft.setRotation(1);

    sdAvailable = SD.begin(SD_CS);
    if (!sdAvailable) {
        Serial.println("microSD not present or failed to init");
    }

    connectWifi();
    syncRtcFromNtpIfPossible();

    digitalWrite(STATUS_LED_PIN, wifiConnected ? HIGH : LOW);
}

void loop() {
    DateTime now = rtc.now();
    drawDashboard(now);

    if (millis() - lastLogMs >= LOG_INTERVAL_MS) {
        lastLogMs = millis();
        logToSd(now);
    }

    delay(1000);
}
