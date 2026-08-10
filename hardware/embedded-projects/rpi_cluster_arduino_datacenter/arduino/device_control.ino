/*
 * Remote device control node: exposes a simple serial command interface so
 * a Raspberry Pi (or any host) can turn devices on/off and query status.
 *
 * Commands (newline-terminated, sent over USB serial at 115200 baud):
 *   ON <pin>      -> set digital pin HIGH
 *   OFF <pin>     -> set digital pin LOW
 *   STATUS        -> report the state of all managed pins as CSV
 *
 * Example: a Pi node in the cluster runs a Python script that opens the
 * serial port and sends "ON 5\n" to energize a relay on pin 5.
 */

const int MANAGED_PINS[] = {2, 3, 4, 5, 6, 7};
const int NUM_PINS = sizeof(MANAGED_PINS) / sizeof(MANAGED_PINS[0]);

String input_line = "";

void setup() {
    Serial.begin(115200);
    for (int i = 0; i < NUM_PINS; i++) {
        pinMode(MANAGED_PINS[i], OUTPUT);
        digitalWrite(MANAGED_PINS[i], LOW);
    }
    Serial.println("device_control ready");
}

void report_status() {
    Serial.print("STATUS");
    for (int i = 0; i < NUM_PINS; i++) {
        Serial.print(",");
        Serial.print(MANAGED_PINS[i]);
        Serial.print("=");
        Serial.print(digitalRead(MANAGED_PINS[i]));
    }
    Serial.println();
}

void handle_command(const String &line) {
    if (line.startsWith("ON ") || line.startsWith("OFF ")) {
        bool turn_on = line.startsWith("ON ");
        int pin = line.substring(line.indexOf(' ') + 1).toInt();

        bool valid = false;
        for (int i = 0; i < NUM_PINS; i++) {
            if (MANAGED_PINS[i] == pin) {
                valid = true;
                break;
            }
        }

        if (valid) {
            digitalWrite(pin, turn_on ? HIGH : LOW);
            Serial.print("OK ");
            Serial.println(line);
        } else {
            Serial.print("ERR unmanaged pin: ");
            Serial.println(pin);
        }
    } else if (line == "STATUS") {
        report_status();
    } else {
        Serial.print("ERR unknown command: ");
        Serial.println(line);
    }
}

void loop() {
    while (Serial.available() > 0) {
        char c = Serial.read();
        if (c == '\n') {
            input_line.trim();
            if (input_line.length() > 0) {
                handle_command(input_line);
            }
            input_line = "";
        } else {
            input_line += c;
        }
    }
}
