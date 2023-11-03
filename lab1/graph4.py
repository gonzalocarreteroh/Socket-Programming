from MM1K import MM1KQueueSimulator

# Simulate M/M/1/K Queue for different values of rho
rhos = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
average_packet_counts1 = []
average_packet_counts2 = []
average_packet_counts3 = []
# Simulation time
T = 1000
average_packet_length = 2000
transmission_rate = 1000000
K = 10
print("MM1K Plot p_loss vs. rho")

for rho in rhos:
    # Compute arrival rate for given rho
    arrival_rate = rho * transmission_rate / average_packet_length
    simulator1 = MM1KQueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K)
    # Get Ploss from first simulator
    p_loss1 = simulator1.run_simulation()[2]
    average_packet_counts1.append(p_loss1)
    print(f"rho = {rho}, K = 10, P(loss) = {p_loss1}")
    simulator2 = MM1KQueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K + 15)
    # Get Ploss from second simulator
    p_loss2 = simulator2.run_simulation()[2]
    average_packet_counts2.append(p_loss2)
    print(f"rho = {rho}, K = 25, P(loss) = {p_loss2}")
    simulator3 = MM1KQueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K + 40)
    # Get Ploss from third simulator
    p_loss3 = simulator3.run_simulation()[2]
    average_packet_counts3.append(p_loss3)
    print(f"rho = {rho}, K = 50, P(loss) = {p_loss3}")


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # Plot P(loss) vs. rho
    plt.plot(rhos, average_packet_counts1, label = 'K = 10', color = 'blue', marker = 'o',
             markerfacecolor = 'blue', markersize = 5)
    plt.plot(rhos, average_packet_counts2, label = 'K = 25', color = 'red',marker = 'o',
             markerfacecolor = 'red', markersize = 5)
    plt.plot(rhos, average_packet_counts3, label = 'K = 50', color = 'green', marker = 'o',
             markerfacecolor = 'green', markersize = 5)

    plt.legend()
    plt.xlabel('rho')
    plt.ylabel('P(loss)')
    plt.title('P(loss) in M/M/1/K Queue')
    plt.show()
