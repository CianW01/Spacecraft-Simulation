
from dataclasses import dataclass


@dataclass
class PowerSystem:
    """Simplified spacecraft electrical power subsystem."""

    battery_capacity_wh: float
    battery_energy_wh: float
    solar_array_power_w: float
    normal_load_w: float
    safe_mode_w: float

    safe_mode: bool = False

    safe_mode_enter_percent: float = 40.0
    safe_mode_exit_percent: float = 50.0

    def __post_init__(self):
        if self.battery_capacity_wh <= 0:
            raise ValueError("Battery capacity must be positive.")

        if not 0 <= self.battery_energy_wh <= self.battery_capacity_wh:
            raise ValueError("Invalid initial battery energy.")

        if not 0 < self.safe_mode_enter_percent < self.safe_mode_exit_percent <= 100:
            raise ValueError("Invalid safe mode thresholds.")

    def update(
        self,
        timestep_seconds: float,
        sunlight_fraction: float = 1.0
    ) -> dict:

        if timestep_seconds <= 0:
            raise ValueError("Timestep must be positive.")

        if not 0.0 <= sunlight_fraction <= 1.0:
            raise ValueError("Sunlight fraction must be between 0 and 1.")

        # Calculate current battery charge
        state_of_charge = (
            self.battery_energy_wh / self.battery_capacity_wh
        ) * 100

        # Automatically manage safe mode
        if not self.safe_mode and state_of_charge <= self.safe_mode_enter_percent:
            self.safe_mode = True

        elif self.safe_mode and state_of_charge >= self.safe_mode_exit_percent:
            self.safe_mode = False

        # Calculate solar generation
        solar_power = self.solar_array_power_w * sunlight_fraction

        # Select electrical load
        load_power = (
            self.safe_mode_w if self.safe_mode
            else self.normal_load_w
        )

        # Convert seconds to hours
        timestep_hours = timestep_seconds / 3600

        # Calculate energy generated and consumed
        solar_energy = solar_power * timestep_hours
        load_energy = load_power * timestep_hours

        previous_energy = self.battery_energy_wh

        # Calculate energy available after consumption
        available_energy = previous_energy + solar_energy

        # Detect energy demand that cannot be supplied
        unmet_energy = max(0.0, load_energy - available_energy)

        # Update battery, respecting capacity limits
        self.battery_energy_wh = max(
            0.0,
            min(
                self.battery_capacity_wh,
                available_energy - load_energy
            )
        )

        # Calculate new battery charge
        state_of_charge = (
            self.battery_energy_wh / self.battery_capacity_wh
        ) * 100

        return {
            "solar_power_w": solar_power,
            "load_power_w": load_power,
            "battery_energy_wh": self.battery_energy_wh,
            "state_of_charge_percent": state_of_charge,
            "unmet_energy_wh": unmet_energy,
            "safe_mode": self.safe_mode
        }

