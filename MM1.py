import random
import math
import queue

# Define simulation time (T) and arrival rate (lambda)
T = 1000  # Adjust the simulation time as needed
arrival_rate = 10.0  # Packets per second

# Define service rate (mu)
service_rate = 500.0  # Packets per second

# For M/M/1/K queue, define the buffer size (K)
K = None  # Set to None for M/M/1 queue, or a positive integer for M/M/1/K queue

# Initialize simulation clock and other variables
clock = 0

packet_counter = 0  # Counter to keep track of packet arrivals
departure_time = math.inf  # Initialize departure time to infinity (no packet in service)

arrival_events = queue.Queue() # List to store arrival events

events = []

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
        'type': "arrival",
        'time': clock,
    }

    events.append(packet)

    arrival_events.put(packet)


departure_events = []

clock = 0

while not arrival_events.empty():

    curr_event = arrival_events.get()

    if clock < curr_event["time"]:
        clock = curr_event["time"]

    service_time = generate_exponential(service_rate)

    clock += service_time

    packet = {
        "type": "departure",
        'time': clock
    }

    events.append(packet)

    packet_counter -= 1

clock = 0
# Generate observer events
observer_lambda = 5 * arrival_rate  # Adjust the rate of observer events as needed
while clock < T:
    observer_time = generate_exponential(observer_lambda)
    clock += observer_time

    events.append({
        "type": "observer",
        'time': clock
    })

events.sort(key = lambda x: x["time"])

Na = 0 #Number of Arrivals
Nd = 0 #Number of departures
No = 0 #Number of observers

Pidle = 0
sum_queue_length_observed = 0

prev_idle = 0
prev_time = None

for event in events:
    if event["type"] == "arrival":
        Na += 1
    elif event["type"] == "departure":
        Nd += 1
    else:
        if Na == Nd:
            if prev_idle == 1:
                Pidle += event["time"] - prev_time
            prev_idle = 1
            prev_time = event["time"]
        else:
            prev_idle = 1
            prev_time = event["time"]

        sum_queue_length_observed += (Na-Nd)
        No += 1

average_queue_length = sum_queue_length_observed / No
idle_ratio = Pidle / T

print(f"Average Queue Length: {average_queue_length}")
print(f"Idle Ratio: {idle_ratio}")
