/*
 * ESP32-05 -- UART GPS Logger
 *
 * Reads NMEA sentences from a GPS module on hardware UART2, parses them
 * with TinyGPS++, shows a live fix on an SSD1306 OLED (I2C), and appends
 * each fix to a CSV track log in LittleFS.
 *
 * Libraries: TinyGPSPlus (mikalhart), Adafruit SSD1306, Adafruit GFX Library.
 *
 * See ../README.md for the full pinout table.
 */

#include <HardwareSerial.h>
#include <TinyGPSPlus.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <LittleFS.h>

const int GPS_RX_PIN = 16; // ESP32 RX2 <- GPS TX
const int GPS_TX_PIN = 17; // ESP32 TX2 -> GPS RX (optional)
const uint32_t GPS_BAUD = 9600;
const int STATUS_LED_PIN = 2;
const unsigned long LOG_INTERVAL_MS = 5000; // write a track point every 5s once fixed

HardwareSerial gpsSerial(2); // UART2
TinyGPSPlus gps;
Adafruit_SSD1306 display(128, 64, &Wire, -1);

unsigned long lastFlashLogMs = 0;
unsigned long lastDisplayMs = 0;
unsigned long lastBlinkMs = 0;
bool ledState = false;

void initLogFile() {
    if (!LittleFS.begin(true)) { // format on first boot if needed
        Serial.println("LittleFS mount failed");
        return;
    }
    if (!LittleFS.exists("/track_log.csv")) {
        File f = LittleFS.open("/track_log.csv", "w");
        if (f) {
            f.println("timestamp_utc,lat,lon,alt_m,speed_kmh,sats");
            f.close();
        }
    }
}

void logFixToFlash() {
    File f = LittleFS.open("/track_log.csv", "a");
    if (!f) return;

    f.printf("%04d-%02d-%02dT%02d:%02d:%02dZ,%.6f,%.6f,%.1f,%.1f,%d\n",
              gps.date.year(), gps.date.month(), gps.date.day(),
              gps.time.hour(), gps.time.minute(), gps.time.second(),
              gps.location.lat(), gps.location.lng(),
              gps.altitude.meters(), gps.speed.kmph(), gps.satellites.value());
    f.close();
}

void updateDisplay() {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);

    if (gps.location.isValid()) {
        display.printf("Lat: %.5f\n", gps.location.lat());
        display.printf("Lon: %.5f\n", gps.location.lng());
        display.printf("Alt: %.1f m\n", gps.altitude.meters());
        display.printf("Spd: %.1f km/h\n", gps.speed.kmph());
        display.printf("Sats: %d\n", gps.satellites.value());
    } else {
        display.println("Waiting for fix...");
        display.printf("Sats visible: %d\n", gps.satellites.value());
    }
    display.display();
}

void setup() {
    Serial.begin(115200);
    pinMode(STATUS_LED_PIN, OUTPUT);

    gpsSerial.begin(GPS_BAUD, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN);

    Wire.begin(21, 22);
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("SSD1306 init failed");
    }

    initLogFile();
    Serial.println("gps_logger ready");
}

void loop() {
    // Feed every available byte to the parser -- NMEA sentences arrive
    // continuously and asynchronously, so we can't just block-read a line.
    while (gpsSerial.available() > 0) {
        gps.encode(gpsSerial.read());
    }

    unsigned long now = millis();

    // Blink while unfixed, solid LED once we have a valid location.
    if (gps.location.isValid()) {
        digitalWrite(STATUS_LED_PIN, HIGH);
    } else if (now - lastBlinkMs > 500) {
        lastBlinkMs = now;
        ledState = !ledState;
        digitalWrite(STATUS_LED_PIN, ledState);
    }

    if (now - lastDisplayMs > 1000) { // refresh display at ~1Hz
        lastDisplayMs = now;
        updateDisplay();
    }

    if (gps.location.isValid() && now - lastFlashLogMs > LOG_INTERVAL_MS) {
        lastFlashLogMs = now;
        logFixToFlash();
    }
}
