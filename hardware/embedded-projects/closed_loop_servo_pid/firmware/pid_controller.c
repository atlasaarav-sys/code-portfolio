#include "pid_controller.h"

static float clamp(float value, float lo, float hi) {
    if (value < lo) return lo;
    if (value > hi) return hi;
    return value;
}

void pid_init(PIDController *pid, float kp, float ki, float kd,
              float output_min, float output_max) {
    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
    pid->has_prev_error = 0;
    pid->output_min = output_min;
    pid->output_max = output_max;
    /* Clamp the integral term to the output range to limit windup. */
    pid->integral_min = output_min;
    pid->integral_max = output_max;
}

void pid_reset(PIDController *pid) {
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
    pid->has_prev_error = 0;
}

float pid_update(PIDController *pid, float setpoint, float measurement, float dt) {
    if (dt <= 0.0f) {
        return 0.0f;
    }

    float error = setpoint - measurement;

    pid->integral += error * dt;
    pid->integral = clamp(pid->integral, pid->integral_min, pid->integral_max);

    float derivative = 0.0f;
    if (pid->has_prev_error) {
        derivative = (error - pid->prev_error) / dt;
    }
    pid->prev_error = error;
    pid->has_prev_error = 1;

    float output = pid->kp * error + pid->ki * pid->integral + pid->kd * derivative;
    return clamp(output, pid->output_min, pid->output_max);
}
