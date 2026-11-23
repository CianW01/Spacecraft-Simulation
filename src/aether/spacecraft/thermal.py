
from dataclasses import dataclass


@dataclass
class ThermalSystem:
    """Simplified spacecraft thermal management subsystem."""

    temperature_k: float = 293.15
    heat_capacity_j_per_k: float = 20000.0

    electronics_heat_w: float = 40.0
    solar_heat_w: float = 60.0

    radiator_conductance_w_per_k: float = 0.5
    radiator_sink_temperature_k: float = 200.0

    minimum_temperature_k: float = 273.15
    maximum_temperature_k: float = 323.15

    def __post_init__(self):

        if self.temperature_k <= 0:
            raise ValueError("Temperature must be above absolute zero.")

        if self.heat_capacity_j_per_k <= 0:
            raise ValueError("Heat capacity must be positive.")

        if self.radiator_conductance_w_per_k < 0:
            raise ValueError("Radiator conductance cannot be negative.")

        if self.minimum_temperature_k >= self.maximum_temperature_k:
            raise ValueError("Invalid temperature limits.")

    def update(
        self,
        timestep_seconds: float,
        sunlight_fraction: float = 1.0
    ) -> dict:

        if timestep_seconds <= 0:
            raise ValueError("Timestep must be positive.")

        if not 0.0 <= sunlight_fraction <= 1.0:
            raise ValueError("Sunlight fraction must be between 0 and 1.")

        # Calculate absorbed solar heat
        solar_heat = self.solar_heat_w * sunlight_fraction

        # Calculate heat lost through the radiator
        radiator_heat_loss = (
            self.radiator_conductance_w_per_k
            * (self.temperature_k - self.radiator_sink_temperature_k)
        )

        # Calculate total heat entering or leaving the spacecraft
        net_heat_power = (
            self.electronics_heat_w
            + solar_heat
            - radiator_heat_loss
        )

        # Calculate temperature change
        energy_change = net_heat_power * timestep_seconds

        temperature_change = (
            energy_change / self.heat_capacity_j_per_k
        )

        self.temperature_k = max(
            0.0,
            self.temperature_k + temperature_change
        )

        # Convert Kelvin to Celsius
        temperature_c = self.temperature_k - 273.15

        # Monitor thermal operating limits
        if self.temperature_k < self.minimum_temperature_k:
            thermal_status = "COLD"

        elif self.temperature_k > self.maximum_temperature_k:
            thermal_status = "HOT"

        else:
            thermal_status = "NOMINAL"

        return {
            "temperature_k": self.temperature_k,
            "temperature_c": temperature_c,
            "solar_heat_w": solar_heat,
            "electronics_heat_w": self.electronics_heat_w,
            "radiator_heat_loss_w": radiator_heat_loss,
            "thermal_status": thermal_status
        }
