from .power import PowerSystem
from .thermal import ThermalSystem
from ..simulation.engine import SimulationEngine
from .attitude import AttitudeSystem
from .communications import CommunicationsSystem
from ..simulation.orbit import GroundStationPass


print("AETHER IS RUNNING!")

# Initialise simulation engine
engine = SimulationEngine(timestep_seconds=60)

# Initialise spacecraft power system
spacecraft_power = PowerSystem(
    battery_capacity_wh=500.0,
    battery_energy_wh=400.0,
    solar_array_power_w=120.0,
    normal_load_w=80.0,
    safe_mode_w=30.0
)
spacecraft_thermal = ThermalSystem()
spacecraft_attitude = AttitudeSystem()
spacecraft_communications = CommunicationsSystem()

# Register power system with simulation engine
engine.register_subsystem("power", spacecraft_power)
engine.register_subsystem("thermal", spacecraft_thermal)
engine.register_subsystem("attitude", spacecraft_attitude)
engine.register_subsystem(
    "communications",
    spacecraft_communications
)

# Initialise ground station pass model
ground_station_pass = GroundStationPass()

def get_ground_station_pass_state():

    mission_time = (
        engine.elapsed_seconds
        + engine.timestep_seconds / 2
    )

    return ground_station_pass.calculate(mission_time)

print("\nAETHER SPACECRAFT SIMULATION")
print("----------------------------------")


# PHASE 1: NORMAL SUNLIGHT
print("\nPHASE 1: NORMAL SUNLIGHT")
print("------------------------")

for minute in range(1, 11):

    pass_state = get_ground_station_pass_state()

    telemetry = engine.advance(
    subsystem_inputs={
        "power": {"sunlight_fraction": 1.0},
        "thermal": {"sunlight_fraction": 1.0},
        "attitude": {"target_angle_deg": 90.0},
        "communications": {
            "distance_m": pass_state["distance_m"],
            "visible": pass_state["visible"]
        }
    }
)  

    power_data = telemetry["power"]
    thermal_data = telemetry["thermal"]
    attitude_data = telemetry["attitude"]
    communications_data = telemetry["communications"]

    print(f"\nMission time: {engine.get_mission_time()}")
    print(f"Solar generation: {power_data['solar_power_w']:.2f} W")
    print(f"Electrical load: {power_data['load_power_w']:.2f} W")
    print(f"Battery energy: {power_data['battery_energy_wh']:.2f} Wh")
    print(f"Battery charge: {power_data['state_of_charge_percent']:.2f}%")
    print(f"Safe mode: {power_data['safe_mode']}")
    print(f"Spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
    print(f"Thermal status: {thermal_data['thermal_status']}")
    print(f"Spacecraft orientation: {attitude_data['current_angle_deg']:.2f}°")
    print(f"Target orientation: {attitude_data['target_angle_deg']:.2f}°")
    print(f"Orientation error: {attitude_data['orientation_error_deg']:.2f}°")
    print(
        f"Ground station visibility: "
        f"{pass_state['visible']}"
    )
    print(
        f"Satellite elevation: "
        f"{pass_state['elevation_deg']:.2f}°"
    )
    print(
        f"Satellite distance: "
        f"{communications_data['distance_m'] / 1000:.2f} km"
    )
    print(f"Link status: {communications_data['link_status']}")
    print(f"Received signal: {communications_data['received_power_dbm']:.2f} dBm")
    print(f"Signal-to-noise ratio: {communications_data['snr_db']:.2f} dB")
    print(f"Link margin: {communications_data['link_margin_db']:.2f} dB")
    print(
        f"Channel capacity: "
        f"{communications_data['channel_capacity_bps'] / 1_000_000:.2f} Mbps"
    )


# PHASE 2: ORBITAL ECLIPSE
print("\nENTERING ORBITAL ECLIPSE")
print("-------------------------")

previous_safe_mode = spacecraft_power.safe_mode

for minute in range(1, 201):

    pass_state = get_ground_station_pass_state()

    telemetry = engine.advance(
    subsystem_inputs={
        "power": {"sunlight_fraction": 0.0},
        "thermal": {"sunlight_fraction": 0.0},
        "attitude": {"target_angle_deg": 180.0},
        "communications": {
            "distance_m": pass_state["distance_m"],
            "visible": pass_state["visible"]
        }
    }
)

    power_data = telemetry["power"]
    thermal_data = telemetry["thermal"]
    attitude_data = telemetry["attitude"]
    communications_data = telemetry["communications"]

    if minute % 10 == 0 or power_data["safe_mode"] != previous_safe_mode:

        print(f"\nMission time: {engine.get_mission_time()}")
        print(f"Eclipse minute: {minute}")
        print(f"Solar generation: {power_data['solar_power_w']:.2f} W")
        print(f"Battery: {power_data['state_of_charge_percent']:.2f}%")
        print(f"Electrical load: {power_data['load_power_w']:.2f} W")
        print(f"Safe mode: {power_data['safe_mode']}")
        print(f"Spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
        print(f"Thermal status: {thermal_data['thermal_status']}")
        print(f"Spacecraft orientation: {attitude_data['current_angle_deg']:.2f}°")
        print(f"Target orientation: {attitude_data['target_angle_deg']:.2f}°")
        print(f"Orientation error: {attitude_data['orientation_error_deg']:.2f}°")
        print(
            f"Ground station visibility: "
            f"{pass_state['visible']}"
        )
        print(
            f"Satellite elevation: "
            f"{pass_state['elevation_deg']:.2f}°"
        )
        print(
            f"Satellite distance: "
            f"{communications_data['distance_m'] / 1000:.2f} km"
        )
        print(f"Link status: {communications_data['link_status']}")
        print(f"Received signal: {communications_data['received_power_dbm']:.2f} dBm")
        print(f"Signal-to-noise ratio: {communications_data['snr_db']:.2f} dB")
        print(f"Link margin: {communications_data['link_margin_db']:.2f} dB")
        print(
            f"Channel capacity: "
            f"{communications_data['channel_capacity_bps'] / 1_000_000:.2f} Mbps"
        )

    previous_safe_mode = power_data["safe_mode"]


# PHASE 3: SUNLIGHT RECOVERY
print("\nEXITING ORBITAL ECLIPSE")
print("-------------------------")

for minute in range(1, 71):

    pass_state = get_ground_station_pass_state()

    telemetry = engine.advance(
    subsystem_inputs={
        "power": {"sunlight_fraction": 1.0},
        "thermal": {"sunlight_fraction": 1.0},
        "attitude": {"target_angle_deg": 0.0},
        "communications": {
            "distance_m": pass_state["distance_m"],
            "visible": pass_state["visible"]
        }
    }
)

    power_data = telemetry["power"]
    thermal_data = telemetry["thermal"]
    attitude_data = telemetry["attitude"]
    communications_data = telemetry["communications"]

    if minute % 5 == 0 or power_data["safe_mode"] != previous_safe_mode:

        print(f"\nMission time: {engine.get_mission_time()}")
        print(f"Recovery minute: {minute}")
        print(f"Solar generation: {power_data['solar_power_w']:.2f} W")
        print(f"Battery: {power_data['state_of_charge_percent']:.2f}%")
        print(f"Electrical load: {power_data['load_power_w']:.2f} W")
        print(f"Safe mode: {power_data['safe_mode']}")
        print(f"Spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
        print(f"Thermal status: {thermal_data['thermal_status']}")
        print(f"Spacecraft orientation: {attitude_data['current_angle_deg']:.2f}°")
        print(f"Target orientation: {attitude_data['target_angle_deg']:.2f}°")
        print(f"Orientation error: {attitude_data['orientation_error_deg']:.2f}°")
        print(
            f"Ground station visibility: "
            f"{pass_state['visible']}"
        )
        print(
            f"Satellite elevation: "
            f"{pass_state['elevation_deg']:.2f}°"
        )
        print(
            f"Satellite distance: "
            f"{communications_data['distance_m'] / 1000:.2f} km"
        )
        print(f"Link status: {communications_data['link_status']}")
        print(f"Received signal: {communications_data['received_power_dbm']:.2f} dBm")
        print(f"Signal-to-noise ratio: {communications_data['snr_db']:.2f} dB")
        print(f"Link margin: {communications_data['link_margin_db']:.2f} dB")
        print(
            f"Channel capacity: "
            f"{communications_data['channel_capacity_bps'] / 1_000_000:.2f} Mbps"
        )

    previous_safe_mode = power_data["safe_mode"]


print("\nMISSION SIMULATION COMPLETE")
print("----------------------------")
print(f"Total mission duration: {engine.get_mission_time()}")
print(f"Final battery charge: {power_data['state_of_charge_percent']:.2f}%")
print(f"Final spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
print(f"Final thermal status: {thermal_data['thermal_status']}")
print(f"Final safe mode status: {power_data['safe_mode']}")
print(f"Final spacecraft orientation: {attitude_data['current_angle_deg']:.2f}°")
print(f"Final orientation error: {attitude_data['orientation_error_deg']:.2f}°")