import matplotlib.pyplot as plt
"""
Repeat the same process for PIDLE and PLOSS as a function of ρ for M/M/1/K queue with different buffer sizes (K).

"""
# Simulate M/M/1 Queue for different values of ρ
rhos = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
average_packet_counts = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

#for rho in rhos:
    # Simulate the queue
    # Calculate E[N] and append to average_packet_counts

# Plot E[N] vs. ρ
plt.plot(rhos, average_packet_counts)
plt.xlabel('ρ')
plt.ylabel('E[N]')
plt.title('Average Number of Packets in M/M/1 Queue')
plt.show()
