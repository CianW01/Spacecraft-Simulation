from .power import PowerSystem
from .thermal import ThermalSystem
from ..simulation.engine import SimulationEngine


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

# Register power system with simulation engine
engine.register_subsystem("power", spacecraft_power)
engine.register_subsystem("thermal", spacecraft_thermal)


print("\nAETHER SPACECRAFT SIMULATION")
print("----------------------------------")


# PHASE 1: NORMAL SUNLIGHT
print("\nPHASE 1: NORMAL SUNLIGHT")
print("------------------------")

for minute in range(1, 11):

    telemetry = engine.advance(
        environment={"sunlight_fraction": 1.0}
    )

    power_data = telemetry["power"]
    thermal_data = telemetry["thermal"]

    print(f"\nMission time: {engine.get_mission_time()}")
    print(f"Solar generation: {power_data['solar_power_w']:.2f} W")
    print(f"Electrical load: {power_data['load_power_w']:.2f} W")
    print(f"Battery energy: {power_data['battery_energy_wh']:.2f} Wh")
    print(f"Battery charge: {power_data['state_of_charge_percent']:.2f}%")
    print(f"Safe mode: {power_data['safe_mode']}")
    print(f"Spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
    print(f"Thermal status: {thermal_data['thermal_status']}")


# PHASE 2: ORBITAL ECLIPSE
print("\nENTERING ORBITAL ECLIPSE")
print("-------------------------")

previous_safe_mode = spacecraft_power.safe_mode

for minute in range(1, 201):

    telemetry = engine.advance(
        environment={"sunlight_fraction": 0.0}
    )

    power_data = telemetry["power"]
    thermal_data = telemetry["thermal"]

    if minute % 10 == 0 or power_data["safe_mode"] != previous_safe_mode:

        print(f"\nMission time: {engine.get_mission_time()}")
        print(f"Eclipse minute: {minute}")
        print(f"Solar generation: {power_data['solar_power_w']:.2f} W")
        print(f"Battery: {power_data['state_of_charge_percent']:.2f}%")
        print(f"Electrical load: {power_data['load_power_w']:.2f} W")
        print(f"Safe mode: {power_data['safe_mode']}")
        print(f"Spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
        print(f"Thermal status: {thermal_data['thermal_status']}")

    previous_safe_mode = power_data["safe_mode"]


# PHASE 3: SUNLIGHT RECOVERY
print("\nEXITING ORBITAL ECLIPSE")
print("-------------------------")

for minute in range(1, 71):

    telemetry = engine.advance(
        environment={"sunlight_fraction": 1.0}
    )

    power_data = telemetry["power"]
    thermal_data = telemetry["thermal"]

    if minute % 5 == 0 or power_data["safe_mode"] != previous_safe_mode:

        print(f"\nMission time: {engine.get_mission_time()}")
        print(f"Recovery minute: {minute}")
        print(f"Solar generation: {power_data['solar_power_w']:.2f} W")
        print(f"Battery: {power_data['state_of_charge_percent']:.2f}%")
        print(f"Electrical load: {power_data['load_power_w']:.2f} W")
        print(f"Safe mode: {power_data['safe_mode']}")
        print(f"Spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
        print(f"Thermal status: {thermal_data['thermal_status']}")

    previous_safe_mode = power_data["safe_mode"]


print("\nMISSION SIMULATION COMPLETE")
print("----------------------------")
print(f"Total mission duration: {engine.get_mission_time()}")
print(f"Final battery charge: {power_data['state_of_charge_percent']:.2f}%")
print(f"Final spacecraft temperature: {thermal_data['temperature_c']:.2f} °C")
print(f"Final thermal status: {thermal_data['thermal_status']}")
print(f"Final safe mode status: {power_data['safe_mode']}")
