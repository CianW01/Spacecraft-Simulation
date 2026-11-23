
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

    def advance(self, environment=None):

        if environment is None:
            environment = {}

        telemetry = {}

        for name, subsystem in self.subsystems.items():

            readings = subsystem.update(
                timestep_seconds=self.timestep_seconds,
                **environment
            )

            telemetry[name] = readings

        self.elapsed_seconds += self.timestep_seconds

        return telemetry

    def get_mission_time(self):

        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"
