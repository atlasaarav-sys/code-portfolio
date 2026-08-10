"""Discrete simulation of a simple DC-servo plant: rotational inertia J
driven by motor torque (proportional to control effort) opposed by viscous
damping B. This is the plant that pid_controller.c/.py is meant to control.

theta'' = (Kt * effort - B * theta') / J
"""

from dataclasses import dataclass


@dataclass
class DCServoPlant:
    J: float = 0.02   # rotational inertia (kg*m^2, arbitrary units for the demo)
    B: float = 0.8     # viscous damping coefficient
    Kt: float = 6.0    # torque constant (effort -> torque)

    position: float = 0.0  # degrees
    velocity: float = 0.0  # degrees/sec

    def reset(self, position=0.0, velocity=0.0):
        self.position = position
        self.velocity = velocity

    def step(self, effort: float, dt: float):
        accel = (self.Kt * effort - self.B * self.velocity) / self.J
        self.velocity += accel * dt
        self.position += self.velocity * dt
        return self.position
