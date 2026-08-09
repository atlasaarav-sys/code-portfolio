#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

typedef struct {
    float kp;
    float ki;
    float kd;

    float integral;
    float prev_error;
    int has_prev_error; /* 0 until the first update() call */

    float integral_min;
    float integral_max;
    float output_min;
    float output_max;
} PIDController;

void pid_init(PIDController *pid, float kp, float ki, float kd,
              float output_min, float output_max);

/* dt in seconds. Returns the control effort, clamped to [output_min, output_max]. */
float pid_update(PIDController *pid, float setpoint, float measurement, float dt);

void pid_reset(PIDController *pid);

#endif /* PID_CONTROLLER_H */
