/*
 * ESP32-01 -- Blink + Button Dev Board firmware
 *
 * Toggles the user LED (D2, GPIO2) every time the user button (SW3, GPIO4)
 * is pressed, with software debounce. This is the "hello world" firmware
 * for the reference board every later ESP32 project in this repo builds
 * physically on top of.
 *
 * Pin mapping (see ../README.md section 1 for the full schematic):
 *   GPIO2  -> D2 user LED (through R2)
 *   GPIO4  -> SW3 user button (active LOW, internal pull-up enabled here)
 */

const int LED_PIN = 2;
const int BUTTON_PIN = 4;
const unsigned long DEBOUNCE_MS = 30;

bool ledState = false;
int lastButtonReading = HIGH;
int debouncedButtonState = HIGH;
unsigned long lastDebounceTime = 0;

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP); // button pulls LOW when pressed
    digitalWrite(LED_PIN, ledState);
    Serial.println("blink_button ready");
}

void loop() {
    int reading = digitalRead(BUTTON_PIN);

    if (reading != lastButtonReading) {
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > DEBOUNCE_MS) {
        if (reading != debouncedButtonState) {
            debouncedButtonState = reading;

            if (debouncedButtonState == LOW) { // button just pressed
                ledState = !ledState;
                digitalWrite(LED_PIN, ledState);
                Serial.print("Button pressed, LED is now ");
                Serial.println(ledState ? "ON" : "OFF");
            }
        }
    }

    lastButtonReading = reading;
}
