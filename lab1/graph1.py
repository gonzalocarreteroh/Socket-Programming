from MM1 import MM1QueueSimulator

# Simulate MM1 Queue for different values of rho
rhos = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
average_packet_counts = []

# Simulator time
T = 1000
average_packet_length = 2000
transmission_rate = 1000000
# Infinite queue
K = None

print("MM1 Plot E[N] vs. rho")

for rho in rhos:
    # Compute arrival rate for given rho
    arrival_rate = rho * transmission_rate / average_packet_length
    simulator = MM1QueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K)
    # Get E[n] from current simulator
    e_n = simulator.run_simulation()[0]
    average_packet_counts.append(e_n)
    print("rho = " + str(rho) + ", E[N] = " + str(e_n))

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # Plot E[N] vs. rho
    plt.plot(rhos, average_packet_counts)
    plt.xlabel('rho')
    plt.ylabel('E(N)')
    plt.title('Average queue length in M/M/1 Queue')
    plt.show()
