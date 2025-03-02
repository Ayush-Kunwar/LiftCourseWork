import matplotlib.pyplot as plt

class Statistics:
    def __init__(self):
        self.total_wait_time = 0
        self.total_travel_time = 0
        self.total_passengers = 0
        self.lift_movements = 0
        self.lift_utilisation = []

    def record_wait_time(self, wait_time):
        """Add to total wait time and track number of passengers."""
        self.total_wait_time += wait_time
        self.total_passengers += 1

    def record_travel_time(self, travel_time):
        """Track total travel time."""
        self.total_travel_time += travel_time

    def record_lift_movement(self):
        """Count the number of times the lift moves."""
        self.lift_movements += 1

    def record_lift_utilization(self, current_capacity, max_capacity):
        """Track how full the lift is on average."""
        utilization = current_capacity / max_capacity
        self.lift_utilisation.append(utilization)

    def generate_statistics(self):
        """Print key statistics for analysis."""
        avg_wait_time = self.total_wait_time / self.total_passengers if self.total_passengers > 0 else 0
        avg_travel_time = self.total_travel_time / self.total_passengers if self.total_passengers > 0 else 0
        avg_utilisation = sum(self.lift_utilisation) / len(self.lift_utilisation) if self.lift_utilisation else 0

        print("\nSimulation Statistics\n")
        print(f"Total Passengers Served: {self.total_passengers}")
        print(f"Total Lift Movements: {self.lift_movements}")
        print(f"Average Wait Time: {avg_wait_time:.2f} Lift movements")
        print(f"Average Travel Time: {avg_travel_time:.2f} Lift movements")
        print(f"Average Lift Utilisation: {avg_utilisation * 100:.2f}%")

    def plot_statistics(self):
        """Generate a plot of lift utilization over time."""
        plt.figure(figsize=(10, 5))
        plt.plot(self.lift_utilisation, marker='o', linestyle='-', color='b', label="Lift Utilisation")
        plt.xlabel("Lift Movements")
        plt.ylabel("Lift Utilisation (fraction)")
        plt.title("Lift Utilisation Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
