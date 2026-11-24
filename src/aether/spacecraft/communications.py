
import math
from dataclasses import dataclass


@dataclass
class CommunicationsSystem:
    """Simplified spacecraft-to-ground-station RF communications model."""

    transmit_power_w: float = 5.0
    frequency_hz: float = 2.2e9

    distance_m: float = 500_000.0

    transmit_antenna_gain_dbi: float = 10.0
    receive_antenna_gain_dbi: float = 10.0

    system_losses_db: float = 2.0

    bandwidth_hz: float = 1_000_000.0
    noise_figure_db: float = 3.0

    required_snr_db: float = 10.0

    SPEED_OF_LIGHT = 299_792_458.0
    BOLTZMANN_DBM_HZ = -174.0

    def __post_init__(self):

        if self.transmit_power_w <= 0:
            raise ValueError("Transmit power must be positive.")

        if self.frequency_hz <= 0:
            raise ValueError("Frequency must be positive.")

        if self.distance_m <= 0:
            raise ValueError("Distance must be positive.")

        if self.bandwidth_hz <= 0:
            raise ValueError("Bandwidth must be positive.")

        if self.system_losses_db < 0:
            raise ValueError("System losses cannot be negative.")

        if self.noise_figure_db < 0:
            raise ValueError("Noise figure cannot be negative.")

    def update(
    self,
    timestep_seconds: float,
    distance_m: float = None,
    visible: bool = True
) -> dict:

        if distance_m is None:
            distance_m = self.distance_m

        if distance_m <= 0:
            raise ValueError("Distance must be positive.")

        self.distance_m = distance_m

        if timestep_seconds <= 0:
            raise ValueError("Timestep must be positive.")

        # Convert transmission power from watts to dBm
        transmit_power_dbm = (
            10 * math.log10(self.transmit_power_w * 1000)
        )

        # Calculate wavelength
        wavelength_m = (
            self.SPEED_OF_LIGHT / self.frequency_hz
        )

        # Free-space path loss using the Friis equation
        path_loss_db = 20 * math.log10(
            (4 * math.pi * distance_m) / wavelength_m
        )

        # Calculate received signal power
        received_power_dbm = (
            transmit_power_dbm
            + self.transmit_antenna_gain_dbi
            + self.receive_antenna_gain_dbi
            - path_loss_db
            - self.system_losses_db
        )

        # Calculate receiver noise power
        noise_power_dbm = (
            self.BOLTZMANN_DBM_HZ
            + 10 * math.log10(self.bandwidth_hz)
            + self.noise_figure_db
        )

        # Calculate signal-to-noise ratio
        snr_db = received_power_dbm - noise_power_dbm

        # Calculate available link margin
        link_margin_db = snr_db - self.required_snr_db

        # Shannon-Hartley theoretical channel capacity
        snr_linear = 10 ** (snr_db / 10)

        channel_capacity_bps = (
            self.bandwidth_hz * math.log2(1 + snr_linear)
        )

        # Determine link status
        if not visible:
            link_status = "OUT_OF_VIEW"

        elif link_margin_db >= 0:
            link_status = "CONNECTED"

        else:
            link_status = "DEGRADED"

        return {
            "transmit_power_dbm": transmit_power_dbm,
            "frequency_hz": self.frequency_hz,
            "wavelength_m": wavelength_m,
            "distance_m": distance_m,
            "path_loss_db": path_loss_db,
            "received_power_dbm": received_power_dbm,
            "noise_power_dbm": noise_power_dbm,
            "snr_db": snr_db,
            "link_margin_db": link_margin_db,
            "channel_capacity_bps": channel_capacity_bps,
            "visible": visible,
            "link_status": link_status
        }
