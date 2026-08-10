/*
 * Smart Energy Monitoring & Optimization System (ESP32)
 *
 * Wiring:
 *   LDR (light) voltage divider -> GPIO34 (ADC1_CH6, input-only)
 *   TMP36 analog temp sensor    -> GPIO35 (ADC1_CH7, input-only)
 *   Relay module IN             -> GPIO26
 *   SSD1306 OLED (I2C)          -> GPIO21 (SDA), GPIO22 (SCL)
 *
 * Decision logic: if the room is bright (LDR reading high) AND the
 * monitored device would otherwise be running (simulated "device on"
 * state), that's wasteful — cut the relay. Same idea for temperature: if
 * it's already cool and heating is on, or already warm and cooling is
 * on, that's wasteful too. A moving-average filter + hysteresis band
 * keep sensor noise from causing relay chatter (false triggers).
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int LIGHT_PIN = 34;
const int TEMP_PIN = 35;
const int RELAY_PIN = 26;

const int SCREEN_WIDTH = 128;
const int SCREEN_HEIGHT = 64;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Moving average filter window (noise reduction).
const int FILTER_WINDOW = 8;
float light_samples[FILTER_WINDOW] = {0};
float temp_samples[FILTER_WINDOW] = {0};
int sample_index = 0;
bool filter_primed = false;

// Thresholds (ADC counts 0-4095 for light, degrees C for temp).
const float LIGHT_BRIGHT_THRESHOLD = 2800.0f;  // room considered "bright"
const float LIGHT_HYSTERESIS = 200.0f;         // avoid chatter at the boundary
const float TEMP_HIGH_THRESHOLD_C = 27.0f;
const float TEMP_HYSTERESIS_C = 1.0f;

bool relay_on = true; // assume device starts on
unsigned long last_sample_ms = 0;
const unsigned long SAMPLE_PERIOD_MS = 50; // 20 Hz, well under the 100ms latency target

float read_temp_c(int adc_raw) {
    float voltage = (adc_raw / 4095.0f) * 3.3f;
    return (voltage - 0.5f) * 100.0f; // TMP36: 10mV/C, 500mV offset at 0C
}

float moving_average(float *buf) {
    float sum = 0;
    for (int i = 0; i < FILTER_WINDOW; i++) sum += buf[i];
    return sum / FILTER_WINDOW;
}

void update_display(float light_avg, float temp_avg, bool relay_state) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print("Light: ");
    display.println(light_avg, 0);
    display.print("Temp:  ");
    display.print(temp_avg, 1);
    display.println(" C");
    display.print("Relay: ");
    display.println(relay_state ? "ON" : "OFF (saving)");
    display.display();
}

bool decide_inefficient_usage(float light_avg, float temp_avg, bool currently_on) {
    // Hysteresis: use a wider "turn off" threshold than "turn back on"
    // threshold so we don't chatter right at the boundary.
    if (currently_on) {
        bool too_bright = light_avg > LIGHT_BRIGHT_THRESHOLD;
        bool too_warm_for_heating = temp_avg > TEMP_HIGH_THRESHOLD_C;
        return !(too_bright || too_warm_for_heating); // stays on unless wasteful
    } else {
        bool dim_enough = light_avg < (LIGHT_BRIGHT_THRESHOLD - LIGHT_HYSTERESIS);
        bool cool_enough = temp_avg < (TEMP_HIGH_THRESHOLD_C - TEMP_HYSTERESIS_C);
        return dim_enough && cool_enough; // only turns back on once clearly justified
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, HIGH);

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("SSD1306 init failed");
    }
}

void loop() {
    unsigned long now = millis();
    if (now - last_sample_ms < SAMPLE_PERIOD_MS) {
        return;
    }
    last_sample_ms = now;

    int light_raw = analogRead(LIGHT_PIN);
    int temp_raw = analogRead(TEMP_PIN);
    float temp_c = read_temp_c(temp_raw);

    light_samples[sample_index] = light_raw;
    temp_samples[sample_index] = temp_c;
    sample_index = (sample_index + 1) % FILTER_WINDOW;
    if (sample_index == 0) filter_primed = true;

    if (!filter_primed) {
        return; // wait for the filter window to fill before deciding anything
    }

    float light_avg = moving_average(light_samples);
    float temp_avg = moving_average(temp_samples);

    relay_on = decide_inefficient_usage(light_avg, temp_avg, relay_on);
    digitalWrite(RELAY_PIN, relay_on ? HIGH : LOW);

    update_display(light_avg, temp_avg, relay_on);

    Serial.print(light_avg);
    Serial.print(",");
    Serial.print(temp_avg);
    Serial.print(",");
    Serial.println(relay_on);
}
