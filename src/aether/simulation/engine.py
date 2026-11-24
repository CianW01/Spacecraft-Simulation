
class SimulationEngine:
    """Central engine for the Aether spacecraft simulation."""

    def __init__(self, timestep_seconds=60):

        if timestep_seconds <= 0:
            raise ValueError("Simulation timestep must be positive.")

        self.timestep_seconds = timestep_seconds
        self.elapsed_seconds = 0

        self.subsystems = {}

    def register_subsystem(self, name, subsystem):

        if name in self.subsystems:
            raise ValueError(f"Subsystem '{name}' already registered.")

        self.subsystems[name] = subsystem

    def advance(self, subsystem_inputs=None):

        if subsystem_inputs is None:
            subsystem_inputs = {}

        # Check that inputs only reference registered subsystems
        unknown_subsystems = (
            set(subsystem_inputs) - set(self.subsystems)
        )

        if unknown_subsystems:
            raise ValueError(
                f"Inputs provided for unregistered subsystems: "
                f"{', '.join(sorted(unknown_subsystems))}"
            )

        telemetry = {}

        # Update each registered subsystem independently
        for name, subsystem in self.subsystems.items():

            inputs = subsystem_inputs.get(name, {})

            if not isinstance(inputs, dict):
                raise TypeError(
                    f"Inputs for '{name}' must be a dictionary."
                )

            readings = subsystem.update(
                timestep_seconds=self.timestep_seconds,
                **inputs
            )

            telemetry[name] = readings

        # Advance the mission clock
        self.elapsed_seconds += self.timestep_seconds

        return telemetry

    def get_mission_time(self):

        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

