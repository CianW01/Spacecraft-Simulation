
from dataclasses import dataclass


@dataclass
class AttitudeSystem:
    """Simplified spacecraft attitude control system."""

    current_angle_deg: float = 0.0
    target_angle_deg: float = 0.0

    angular_velocity_deg_s: float = 0.0
    max_rotation_rate_deg_s: float = 2.0

    def __post_init__(self):

        if self.max_rotation_rate_deg_s <= 0:
            raise ValueError("Maximum rotation rate must be positive.")

    def update(
        self,
        timestep_seconds: float,
        target_angle_deg: float = 0.0
    ) -> dict:

        if timestep_seconds <= 0:
            raise ValueError("Timestep must be positive.")

        self.target_angle_deg = target_angle_deg

        # Calculate the angular difference
        angle_error = (
            self.target_angle_deg - self.current_angle_deg
        )

        # Determine the shortest rotation direction
        angle_error = (angle_error + 180) % 360 - 180

        # Calculate required rotation rate
        rotation_rate = max(
            -self.max_rotation_rate_deg_s,
            min(self.max_rotation_rate_deg_s, angle_error / timestep_seconds)
        )

        # Update spacecraft orientation
        self.angular_velocity_deg_s = rotation_rate

        self.current_angle_deg = (
            self.current_angle_deg
            + self.angular_velocity_deg_s * timestep_seconds
        ) % 360

        # Calculate remaining orientation error
        remaining_error = (
            self.target_angle_deg - self.current_angle_deg + 180
        ) % 360 - 180

        return {
            "current_angle_deg": self.current_angle_deg,
            "target_angle_deg": self.target_angle_deg,
            "angular_velocity_deg_s": self.angular_velocity_deg_s,
            "orientation_error_deg": remaining_error
        }
