import numpy as np
import random
import math

# Define simulation time (T) and arrival rate (lambda)
T = 1000  # Adjust the simulation time as needed
arrival_rate = 10.0  # Packets per second

# Define service rate (mu)
service_rate = 500.0  # Packets per second

# For M/M/1/K queue, define the buffer size (K)
K = None  # Set to None for M/M/1 queue, or a positive integer for M/M/1/K queue

# Initialize simulation clock and other variables
clock = 0
queue = []  # List to represent the queue

packet_counter = 0  # Counter to keep track of packet arrivals
departure_time = math.inf  # Initialize departure time to infinity (no packet in service)
observed_events = []  # List to store observer events


# Function to generate exponential random variable
def generate_exponential(lambda_param):
    u = random.random()  # Generate a random floating-point number between 0 and 1
    return -math.log(1 - u) / lambda_param


# Generate packet arrivals
while clock < T:
    interarrival_time = generate_exponential(arrival_rate)
    clock += interarrival_time
    packet_counter += 1

    # Create packet and add it to the queue
    packet = {
        'id': packet_counter,
        'arrival_time': clock,
    }
    queue.append(packet)

    # If the queue was previously empty, schedule departure
    if departure_time == math.inf:
        service_time = generate_exponential(service_rate)
        departure_time = clock + service_time

# Generate observer events
observer_lambda = 5 * arrival_rate  # Adjust the rate of observer events as needed
while clock < T:
    observer_time = generate_exponential(observer_lambda)
    clock += observer_time

    # Record the state of the queue
    num_packets_in_queue = len(queue)
    server_idle = 1 if departure_time == math.inf else 0
    packet_loss = 0 if K is None else max(0, num_packets_in_queue - K) / packet_counter

    observed_events.append({
        'time': clock,
        'num_packets_in_queue': num_packets_in_queue,
        'server_idle': server_idle,
        'packet_loss': packet_loss,
    })

# Process observer events and calculate metrics
total_idle_time = 0
total_packet_loss = 0

for i in range(1, len(observed_events)):
    time_diff = observed_events[i]['time'] - observed_events[i - 1]['time']
    total_idle_time += observed_events[i - 1]['server_idle'] * time_diff
    total_packet_loss += observed_events[i]['packet_loss'] * time_diff

# Calculate performance metrics
average_queue_length = total_idle_time / T
idle_ratio = total_idle_time / T
packet_loss_ratio = total_packet_loss / T

print(f"Average Queue Length: {average_queue_length}")
print(f"Idle Ratio: {idle_ratio}")
print(f"Packet Loss Ratio: {packet_loss_ratio}")

if __name__ == "__main__":
    # Run the simulator
    # You can adjust the simulation time (T) and other parameters as needed
    # For M/M/1 queue, set K to None
    # For M/M/1/K queue, set K to a positive integer
    pass
