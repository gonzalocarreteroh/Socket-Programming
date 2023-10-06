import heapq
import random
import math


class MM1KQueueSimulator:
    def __init__(self, T, arrival_rate, average_package_length, transmission_rate, K=None):
        self.T = T
        self.arrival_rate = arrival_rate
        self.average_package_length = average_package_length
        self.transmission_rate = transmission_rate
        self.K = K

        self.clock = 0
        self.events = []

    def generate_exponential(self, lambda_param):
        u = random.random()
        return -math.log(1 - u) / lambda_param

    def generate_packet_arrivals(self):
        while self.clock < self.T:
            interarrival_time = self.generate_exponential(self.arrival_rate)
            self.clock += interarrival_time

            packet = (self.clock, "arrival")
            heapq.heappush(self.events, packet)

    def generate_service_time(self):
        package_length = self.generate_exponential(1 / self.average_package_length)
        service_time = package_length / self.transmission_rate
        return service_time

    def generate_observers(self):

        self.clock = 0
        observer_average = 5 * self.arrival_rate
        while self.clock < self.T:
            observer_time = self.generate_exponential(observer_average)
            self.clock += observer_time

            observer = (self.clock, "observer")

            heapq.heappush(self.events, observer)

    def run_simulation(self):
        self.generate_packet_arrivals()
        total_packets = len(self.events)

        self.generate_observers()

        Na = 0  # Number of Arrivals
        Nd = 0  # Number of departures
        No = 0  # Number of observers

        total_idle_count = 0
        sum_queue_length_observed = 0
        dropped_counter = 0
        prev_depart_time = 0

        while self.events:
            event = heapq.heappop(self.events)
            if event[1] == "arrival":
                if abs(Na - Nd - dropped_counter) >= self.K:
                    Na += 1
                    # Buffer is full
                    dropped_counter += 1
                else:
                    Na += 1

                    if prev_depart_time < event[0]:
                        prev_depart_time = event[0]

                    service_time = self.generate_service_time()
                    current_departure_time = prev_depart_time + service_time

                    departure = (current_departure_time, "departure")
                    heapq.heappush(self.events, departure)

                    prev_depart_time = current_departure_time

            elif event[1] == "departure":
                Nd += 1

            else:
                if Na - dropped_counter == Nd:
                    # server is idle
                    total_idle_count += 1

                sum_queue_length_observed += abs(Na - dropped_counter - Nd)
                No += 1

        average_queue_length = sum_queue_length_observed / No
        idle_ratio = total_idle_count / No
        packet_loss_probability = dropped_counter / total_packets

        return average_queue_length, idle_ratio, packet_loss_probability


if __name__ == "__main__":
    # Usage example
    T = 2000
    arrival_rate = 200.0
    average_package_length = 2000
    transmission_rate = 1000000
    K = 50

    simulator = MM1KQueueSimulator(T, arrival_rate, average_package_length, transmission_rate, K)
    print(simulator.run_simulation())
