import random
import math
import queue

class MM1QueueSimulator:
    def __init__(self, T, arrival_rate, average_package_length, transmission_rate, K=None):
        self.T = T
        self.arrival_rate = arrival_rate
        self.average_package_length = average_package_length
        self.transmission_rate = transmission_rate
        self.K = K

        self.clock = 0
        self.arrival_events = queue.Queue()
        self.events = []

    def generate_exponential(self, lambda_param):
        u = random.random()
        return -math.log(1 - u) / lambda_param

    def generate_packet_arrivals(self):
        while self.clock < self.T:
            interarrival_time = self.generate_exponential(self.arrival_rate)
            self.clock += interarrival_time

            packet = {
                'type': "arrival",
                'time': self.clock,
            }

            self.events.append(packet)
            self.arrival_events.put(packet)

    def generate_departures(self):

        self.clock = 0

        while not self.arrival_events.empty():
            curr_event = self.arrival_events.get()

            if self.clock < curr_event["time"]:
                self.clock = curr_event["time"]

            package_length = self.generate_exponential(1 / self.average_package_length)
            service_time = package_length / self.transmission_rate

            self.clock += service_time

            packet = {
                "type": "departure",
                'time': self.clock
            }

            self.events.append(packet)



    def generate_observers(self):

        self.clock = 0
        observer_average = 5 * arrival_rate
        while self.clock < T:
            observer_time = self.generate_exponential(observer_average)
            self.clock += observer_time

            self.events.append({
                "type": "observer",
                'time': self.clock
            })

    def run_simulation(self):
        self.generate_packet_arrivals()
        self.generate_departures()
        self.generate_observers()
        self.events.sort(key = lambda x: x["time"])

        Na = 0  # Number of Arrivals
        Nd = 0  # Number of departures
        No = 0  # Number of observers

        total_idle_count = 0
        sum_queue_length_observed = 0

        for event in self.events:
            if event["type"] == "arrival":
                Na += 1
            elif event["type"] == "departure":
                Nd += 1
            else:
                if Na == Nd:
                    total_idle_count += 1
                sum_queue_length_observed += abs(Na - Nd)
                No += 1

        average_queue_length = sum_queue_length_observed / No
        idle_ratio = total_idle_count / No

        return average_queue_length, idle_ratio

# Usage example
T = 1000
average_package_length = 2000
#average_package_length = 2000
transmission_rate = 1000000
arrival_rate = 1.2 * transmission_rate / average_package_length
K = None

simulator = MM1QueueSimulator(T, arrival_rate, average_package_length, transmission_rate, K)
print(simulator.run_simulation())
