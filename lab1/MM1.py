import random
import math
import queue

class MM1QueueSimulator:
    def __init__(self, T, arrival_rate, average_package_length, transmission_rate, K=None):
        # Simulation time
        self.T = T
        self.arrival_rate = arrival_rate
        self.average_package_length = average_package_length
        self.transmission_rate = transmission_rate
        # Queue size
        self.K = K
        # Track time when generating packets
        self.clock = 0
        self.arrival_events = queue.Queue()
        # Events queue
        self.events = []

    def generate_exponential(self, lambda_param):
        u = random.random()
        return -math.log(1 - u) / lambda_param

    def generate_packet_arrivals(self):
        """Function to generate all arrival events"""
        # Generate arrival events under simulation time
        while self.clock < self.T:
            interarrival_time = self.generate_exponential(self.arrival_rate)
            # Arrival time is prev arrival time + interarrival time
            self.clock += interarrival_time
            # Create arrival event
            packet = {
                'type': "arrival",
                'time': self.clock,
            }
            # Put arrival event at the end of the queue
            self.events.append(packet)
            self.arrival_events.put(packet)

    def generate_departures(self):
        """Function to generate all departure events"""
        self.clock = 0
        # One deparrture event for each arrival event
        while not self.arrival_events.empty():
            # Get an arrival event
            curr_event = self.arrival_events.get()

            if self.clock < curr_event["time"]:
                # The packet doesn't need to wait to be processed
                self.clock = curr_event["time"]

            package_length = self.generate_exponential(1 / self.average_package_length)
            service_time = package_length / self.transmission_rate
            # Update the clock until the time current packet finishes being served
            self.clock += service_time
            # Create departure event
            packet = {
                "type": "departure",
                'time': self.clock
            }
            # Put departure event at the end of the queue
            self.events.append(packet)



    def generate_observers(self):
        """Function to generate all observer events"""
        self.clock = 0
        # Observer average rate is five times grater than arrival's
        observer_average = 5 * self.arrival_rate
        # Generate observer events under simulation time
        while self.clock < self.T:
            observer_time = self.generate_exponential(observer_average)
            # Observer time is prev observer time + new difference computed
            self.clock += observer_time
            # Create observer event and put it at the end of queue
            self.events.append({
                "type": "observer",
                'time': self.clock
            })

    def run_simulation(self):
        """Run the simulation"""
        # Generate all events
        self.generate_packet_arrivals()
        self.generate_departures()
        self.generate_observers()
        # Sort events by time
        self.events.sort(key = lambda x: x["time"])

        Na = 0  # Number of Arrivals
        Nd = 0  # Number of departures
        No = 0  # Number of observers
        # Counters
        total_idle_count = 0
        sum_queue_length_observed = 0
        # Loop through all events in queue
        for event in self.events:
            if event["type"] == "arrival":
                # New arrrival
                Na += 1
            elif event["type"] == "departure":
                # New departure
                Nd += 1
            else:
                """Observer event"""
                if Na == Nd:
                    # Queue is empty
                    total_idle_count += 1
                # Add packets observed in the queue to counter
                sum_queue_length_observed += abs(Na - Nd)
                No += 1
        # Compute statistics
        average_queue_length = sum_queue_length_observed / No
        idle_ratio = total_idle_count / No

        return average_queue_length, idle_ratio

if __name__ == "__main__":
    # Usage example
    T = 1000
    average_package_length = 2000
    #average_package_length = 2000
    transmission_rate = 1000000
    arrival_rate = 1.2 * transmission_rate / average_package_length
    K = None

    simulator = MM1QueueSimulator(T, arrival_rate, average_package_length, transmission_rate, K)
    print(simulator.run_simulation())
