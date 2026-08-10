/*
 * Closed-loop servo position control: potentiometer feedback, PWM motor
 * drive, PID loop run at ~50 Hz.
 *
 * Wiring:
 *   Potentiometer wiper -> A0 (feedback, 0-5V maps to 0-position range)
 *   Motor driver PWM in  -> D9 (direction handled by a second digital pin)
 *   Motor driver DIR     -> D8
 *
 * Uses the portable pid_controller.c/.h core so the same PID math is
 * shared with the STM32 version and the Python simulator.
 */

extern "C" {
#include "pid_controller.h"
}

const int POT_PIN = A0;
const int PWM_PIN = 9;
const int DIR_PIN = 8;

const unsigned long LOOP_PERIOD_MS = 20; // 50 Hz
unsigned long last_loop_ms = 0;

PIDController pid;
float setpoint_deg = 90.0f; // target position, degrees (0-180 potentiometer range)

float read_position_deg() {
    int raw = analogRead(POT_PIN); // 0-1023
    return (raw / 1023.0f) * 180.0f;
}

void drive_motor(float control_effort) {
    // control_effort in [-255, 255]: sign = direction, magnitude = PWM duty
    if (control_effort >= 0) {
        digitalWrite(DIR_PIN, HIGH);
        analogWrite(PWM_PIN, (int)control_effort);
    } else {
        digitalWrite(DIR_PIN, LOW);
        analogWrite(PWM_PIN, (int)(-control_effort));
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(PWM_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);

    // Gains tuned in sim/pid_sim.py against the plant model before porting here.
    pid_init(&pid, 4.0f, 0.5f, 0.15f, -255.0f, 255.0f);
    last_loop_ms = millis();
}

void loop() {
    unsigned long now = millis();
    if (now - last_loop_ms < LOOP_PERIOD_MS) {
        return;
    }
    float dt = (now - last_loop_ms) / 1000.0f;
    last_loop_ms = now;

    float position = read_position_deg();
    float effort = pid_update(&pid, setpoint_deg, position, dt);
    drive_motor(effort);

    Serial.print(position);
    Serial.print(",");
    Serial.println(effort);
}
