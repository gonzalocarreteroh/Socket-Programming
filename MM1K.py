import heapq
import random
import math


class MM1KQueueSimulator:
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
        # Queue
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
            # Generate arrival event
            packet = (self.clock, "arrival")
            # Put event in the "queue" (it is a heap so it is inserted in the position sorted by time)
            heapq.heappush(self.events, packet)

    def generate_service_time(self):
        """Auxiliary function for departures during simulation"""
        package_length = self.generate_exponential(1 / self.average_package_length)
        service_time = package_length / self.transmission_rate
        return service_time

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
            # Create observer event
            observer = (self.clock, "observer")
            # Put observer event into the "queue"
            heapq.heappush(self.events, observer)

    def run_simulation(self):
        """Run the simulation"""
        # Generate arrival and observer events
        self.generate_packet_arrivals()
        self.generate_observers()

        Na = 0  # Number of Arrivals
        Nd = 0  # Number of departures
        No = 0  # Number of observers
        # Counters
        total_idle_count = 0
        sum_queue_length_observed = 0
        dropped_counter = 0
        prev_depart_time = 0
        # Loops through all events in order
        while self.events:
            # Take event with smallest time out of the queue
            event = heapq.heappop(self.events)
            if event[1] == "arrival":
                if abs(Na - Nd - dropped_counter) >= self.K:
                    Na += 1
                    # Buffer is full
                    dropped_counter += 1
                else:
                    # There is space in the queue
                    Na += 1

                    if prev_depart_time < event[0]:
                        # There is no other packet being serviced
                        prev_depart_time = event[0]

                    service_time = self.generate_service_time()
                    # Current departure time is service time + prev departure time
                    current_departure_time = prev_depart_time + service_time
                    # Create departure event
                    departure = (current_departure_time, "departure")
                    # Put departure event in correspinding place in queue
                    heapq.heappush(self.events, departure)

                    prev_depart_time = current_departure_time

            elif event[1] == "departure":
                # Departure event
                Nd += 1

            else:
                if Na - dropped_counter == Nd:
                    # server is idle
                    total_idle_count += 1
                # Add observed packets in queue to counter
                sum_queue_length_observed += abs(Na - dropped_counter - Nd)
                No += 1
        # Compute statistics
        average_queue_length = sum_queue_length_observed / No
        idle_ratio = total_idle_count / No
        packet_loss_probability = dropped_counter / Na

        return average_queue_length, idle_ratio, packet_loss_probability


if __name__ == "__main__":
    # Usage example
    T = 2000
    arrival_rate = 1.5 * 1000000 / 2000
    average_package_length = 2000
    transmission_rate = 1000000
    K = 50

    simulator = MM1KQueueSimulator(T, arrival_rate, average_package_length, transmission_rate, K)
    print(simulator.run_simulation())
