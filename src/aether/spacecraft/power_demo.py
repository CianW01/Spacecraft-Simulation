
from .power import PowerSystem

print("AETHER IS RUNNING!")

spacecraft_power = PowerSystem(
    battery_capacity_wh=500.0,
    battery_energy_wh=400.0,
    solar_array_power_w=120.0,
    normal_load_w=80.0,
    safe_mode_w=30.0
)

print("AETHER SPACECRAFT POWER SIMULATION")
print("----------------------------------")

for minute in range(1, 11):

    telemetry = spacecraft_power.update(
        timestep_seconds=60,
        sunlight_fraction=1.0
    )

    print(f"\nSimulation minute: {minute}")
    print(f"Solar generation: {telemetry['solar_power_w']:.2f} W")
    print(f"Electrical load: {telemetry['load_power_w']:.2f} W")
    print(f"Battery energy: {telemetry['battery_energy_wh']:.2f} Wh")
    print(f"Battery charge: {telemetry['state_of_charge_percent']:.2f}%")


print("\nENTERING ORBITAL ECLIPSE")
print("-------------------------")

previous_safe_mode = spacecraft_power.safe_mode

for minute in range(1, 201):

    telemetry = spacecraft_power.update(
        timestep_seconds=60,
        sunlight_fraction=0.0
    )

    if minute % 10 == 0 or telemetry["safe_mode"] != previous_safe_mode:

        print(f"\nEclipse minute: {minute}")
        print(f"Battery: {telemetry['state_of_charge_percent']:.2f}%")
        print(f"Electrical load: {telemetry['load_power_w']:.2f} W")
        print(f"Safe mode: {telemetry['safe_mode']}")

    previous_safe_mode = telemetry["safe_mode"]


print("\nEXITING ORBITAL ECLIPSE")
print("-------------------------")

for minute in range(1, 71):

    telemetry = spacecraft_power.update(
        timestep_seconds=60,
        sunlight_fraction=1.0
    )

    if minute % 5 == 0 or telemetry["safe_mode"] != previous_safe_mode:

        print(f"\nRecovery minute: {minute}")
        print(f"Battery: {telemetry['state_of_charge_percent']:.2f}%")
        print(f"Electrical load: {telemetry['load_power_w']:.2f} W")
        print(f"Safe mode: {telemetry['safe_mode']}")

    previous_safe_mode = telemetry["safe_mode"]
