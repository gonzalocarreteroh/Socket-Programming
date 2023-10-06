import matplotlib.pyplot as plt
from MM1K import MM1KQueueSimulator

# Simulate M/M/1/K Queue for different values of ρ
rhos = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
average_packet_counts1 = []
average_packet_counts2 = []
average_packet_counts3 = []

T = 1000
average_packet_length = 2000
transmission_rate = 1000000
K = 10

print("MM1K Plot E[n] vs. ρ")

for rho in rhos:
    arrival_rate = rho * transmission_rate / average_packet_length
    simulator1 = MM1KQueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K)
    e_n1 = simulator1.run_simulation()[0]
    average_packet_counts1.append(e_n1)
    print(f"ρ = {rho}, K = 10, E[N] = {e_n1}")
    simulator2 = MM1KQueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K + 15)
    e_n2 = simulator2.run_simulation()[0]
    average_packet_counts2.append(e_n2)
    print(f"ρ = {rho}, K = 25, E[N] = {e_n2}")
    simulator3 = MM1KQueueSimulator(T, arrival_rate, average_packet_length, transmission_rate, K + 40)
    e_n3 = simulator3.run_simulation()[0]
    average_packet_counts3.append(e_n3)
    print(f"ρ = {rho}, K = 50, E[N] = {e_n3}")

if __name__ == "__main__":
    # Plot E[N] vs. ρ
    plt.plot(rhos, average_packet_counts1, label = 'K = 10', color = 'blue', marker = 'o',
             markerfacecolor = 'blue', markersize = 5)
    plt.plot(rhos, average_packet_counts2, label = 'K = 25', color = 'red',marker = 'o',
             markerfacecolor = 'red', markersize = 5)
    plt.plot(rhos, average_packet_counts3, label = 'K = 50', color = 'green', marker = 'o',
             markerfacecolor = 'green', markersize = 5)

    plt.legend()
    plt.xlabel('ρ')
    plt.ylabel('E[n]')
    plt.title('E[n] in M/M/1/K Queue')
    plt.show()
