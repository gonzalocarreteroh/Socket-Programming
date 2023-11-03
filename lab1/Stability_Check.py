from lab1.MM1K import MM1KQueueSimulator
from lab1.MM1 import MM1QueueSimulator

simulator = input("Which simulator do you want to check the stability for (Enter MM1 or MM1K): ")

k = None

if simulator == "MM1":
   rhos = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
else:
   rhos = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
   K = int(input("Choose the value of K: "))


# Values of T you want to compare
T1 = int(input("Select the first value of T to compare with (for example T = 1000): "))
T2 = int(input("Select the second value of T to compare with (for example T = 2000): "))

average_packet_length = 2000
transmission_rate = 1000000

# Store the computed values for each simulation
values1 = {}
values2 = {}

for rho in rhos:
    # Compute arrival rate for given rho
    arrival_rate = rho * transmission_rate / average_packet_length
    if simulator == "MM1":
       # Infinite buffer with T1
       simulator1 = MM1QueueSimulator(T1, arrival_rate, average_packet_length, transmission_rate)
       # Infinite buffer with T2
       simulator2 = MM1QueueSimulator(T2, arrival_rate, average_packet_length, transmission_rate)
    elif simulator == "MM1K":
       # Finite buffer with T1
       simulator1 = MM1KQueueSimulator(T1, arrival_rate, average_packet_length, transmission_rate, K)
       # Finite buffer with T2
       simulator2 = MM1KQueueSimulator(T2, arrival_rate, average_packet_length, transmission_rate, K)
    else:
         print("Wrong simulator name!")
         exit()
       
    # Store values computed in both simulations
    values1[rho] = simulator1.run_simulation()
    values2[rho] = simulator2.run_simulation()

for r in rhos:
  # Store the values computed for each rho
  t1_E = values1[r][0]
  t2_E = values2[r][0]
  t1_Pidle = values1[r][1]
  t2_Pidle = values2[r][1]
  if simulator == "MM1K":
      # Only P(loss) for finite queue
      t1_Ploss = values1[r][2]
      t2_Ploss = values2[r][2]
  # Compute the difference in percentage between both simulations' values
  diff_E = (abs(t1_E - t2_E) / max(1, t1_E)) * 100
  diff_Pidle = (abs(t1_Pidle - t2_Pidle) / max(1,t1_Pidle)) * 100
  if simulator == "MM1K":
        diff_Ploss = (abs(t1_Ploss - t2_Ploss) / max(1,t1_Ploss)) * 100
  # Print the results
  if (simulator == "MM1"):
      print(f"Difference between simulations for {r} is E[n]: {round(diff_E, 3)}%, P(idle): {round(diff_Pidle,3)}%")
  else:
      print(f"Difference between simulations for {r} is E[n]: {round(diff_E,3)}%, P(idle): {round(diff_Pidle,3)}%, P(loss): {round(diff_Ploss,3)}%")

