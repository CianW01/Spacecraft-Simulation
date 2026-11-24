
import math
from dataclasses import dataclass


@dataclass
class GroundStationPass:
    """Simplified satellite pass geometry over a ground station."""

    earth_radius_m: float = 6_371_000.0
    orbital_altitude_m: float = 500_000.0

    pass_duration_seconds: float = 1200.0
    maximum_elevation_deg: float = 80.0

    def __post_init__(self):

        if self.earth_radius_m <= 0:
            raise ValueError("Earth radius must be positive.")

        if self.orbital_altitude_m <= 0:
            raise ValueError("Orbital altitude must be positive.")

        if self.pass_duration_seconds <= 0:
            raise ValueError("Pass duration must be positive.")

        if not 0 < self.maximum_elevation_deg <= 90:
            raise ValueError("Maximum elevation must be between 0 and 90 degrees.")

    def calculate(self, elapsed_seconds: float) -> dict:

        if elapsed_seconds < 0:
            raise ValueError("Elapsed time cannot be negative.")

        visible = elapsed_seconds <= self.pass_duration_seconds

        if visible:

            pass_progress = (
                elapsed_seconds / self.pass_duration_seconds
            )

            elevation_deg = (
                self.maximum_elevation_deg
                * math.sin(math.pi * pass_progress)
            )

        else:
            elevation_deg = 0.0

        elevation_rad = math.radians(elevation_deg)

        earth_radius = self.earth_radius_m
        satellite_radius = (
            self.earth_radius_m + self.orbital_altitude_m
        )

        # Calculate satellite-to-ground-station slant range
        distance_m = (
            math.sqrt(
                satellite_radius ** 2
                - (earth_radius * math.cos(elevation_rad)) ** 2
            )
            - earth_radius * math.sin(elevation_rad)
        )

        return {
            "visible": visible,
            "elevation_deg": elevation_deg,
            "distance_m": distance_m
        }
