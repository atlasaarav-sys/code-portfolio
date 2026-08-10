/*
 * Scheduled automation node: runs a set of timed routines without any host
 * involvement (non-blocking, millis()-based scheduler — no delay()) and
 * reports its own status/heartbeat over serial so a Pi node can confirm
 * it's alive and log what it executed.
 */

struct Routine {
    const char *name;
    int pin;
    unsigned long interval_ms;
    unsigned long last_run_ms;
};

Routine routines[] = {
    {"blink_status_led", 13, 1000, 0},
    {"pulse_relay_a", 5, 5000, 0},
    {"pulse_relay_b", 6, 8000, 0},
};
const int NUM_ROUTINES = sizeof(routines) / sizeof(routines[0]);

unsigned long last_heartbeat_ms = 0;
const unsigned long HEARTBEAT_INTERVAL_MS = 10000;

void setup() {
    Serial.begin(115200);
    for (int i = 0; i < NUM_ROUTINES; i++) {
        pinMode(routines[i].pin, OUTPUT);
    }
    Serial.println("automation_routine ready");
}

void run_routine(Routine &r) {
    digitalWrite(r.pin, !digitalRead(r.pin)); // toggle
    Serial.print("EXEC ");
    Serial.print(r.name);
    Serial.print(" pin=");
    Serial.print(r.pin);
    Serial.print(" t=");
    Serial.println(millis());
}

void loop() {
    unsigned long now = millis();

    for (int i = 0; i < NUM_ROUTINES; i++) {
        if (now - routines[i].last_run_ms >= routines[i].interval_ms) {
            routines[i].last_run_ms = now;
            run_routine(routines[i]);
        }
    }

    if (now - last_heartbeat_ms >= HEARTBEAT_INTERVAL_MS) {
        last_heartbeat_ms = now;
        Serial.print("HEARTBEAT t=");
        Serial.println(now);
    }
}
