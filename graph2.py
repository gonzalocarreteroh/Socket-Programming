import matplotlib.pyplot as plt
from MM1 import MM1QueueSimulator

# Simulate M/M/1 Queue for different values of ρ
rhos = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
average_packet_counts = []


T = 1000
arrival_rate = 200.0
transmission_rate = 1000000
average_packet_length = 2000
K = None

for rho in rhos:
    arrival_rate = rho * transmission_rate / average_packet_length
    simulator = MM1QueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K)
    average_packet_counts.append(simulator.run_simulation()[1])

# Plot E[N] vs. ρ
plt.plot(rhos, average_packet_counts)
plt.xlabel('ρ')
plt.ylabel('P(idle)')
plt.title('P(idle) in M/M/1 Queue')
plt.show()
