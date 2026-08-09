"""Python port of firmware/pid_controller.c, kept 1:1 with the C update
equation so simulation numbers reflect what the embedded code would do.
"""


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


class PIDController:
    def __init__(self, kp, ki, kd, output_min, output_max):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0
        self.has_prev_error = False
        self.output_min = output_min
        self.output_max = output_max
        self.integral_min = output_min
        self.integral_max = output_max

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.has_prev_error = False

    def update(self, setpoint, measurement, dt):
        if dt <= 0:
            return 0.0

        error = setpoint - measurement

        self.integral += error * dt
        self.integral = clamp(self.integral, self.integral_min, self.integral_max)

        derivative = 0.0
        if self.has_prev_error:
            derivative = (error - self.prev_error) / dt
        self.prev_error = error
        self.has_prev_error = True

        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        return clamp(output, self.output_min, self.output_max)
