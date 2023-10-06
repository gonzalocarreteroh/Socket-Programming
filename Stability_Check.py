from MM1K import MM1KQueueSimulator
from MM1 import MM1QueueSimulator

simulator = input("Which simulator do you want to check the stability for (Enter MM1 or MM1K): ")

if simulator == "MM1":
   rhos = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
   K = None
else:
   rhos = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
   K = int(input("Choose the value of K: "))


# Values of T you want to compare
T1 = int(input("Select the first value of T to compare with (for example T = 1000): "))
T2 = int(input("Select the second value of T to compare with (for example T = 2000): "))

average_packet_length = 2000
transmission_rate = 1000000

values1 = {}
values2 = {}

for rho in rhos:
    arrival_rate = rho * transmission_rate / average_packet_length
    if simulator == "MM1":
       simulator1 = MM1QueueSimulator(T1, arrival_rate, average_packet_length, transmission_rate, K)
       simulator2 = MM1QueueSimulator(T2, arrival_rate, average_packet_length, transmission_rate, K)
    else:
       simulator1 = MM1KQueueSimulator(T1, arrival_rate, average_packet_length, transmission_rate, K)
       simulator2 = MM1KQueueSimulator(T2, arrival_rate, average_packet_length, transmission_rate, K)
       
    values1[rho] = simulator1.run_simulation()
    values2[rho] = simulator2.run_simulation()

for r in values1.keys():
  t1_E = values1[r][0]
  t2_E = values2[r][0]
  t1_Pidle = values1[r][1]
  t2_Pidle = values2[r][1]
  if simulator == "MM1K":
      t1_Ploss = values1[r][2]
      t2_Ploss = values2[r][2]

  if t1_E != 0:
    diff_E = (abs(t1_E - t2_E) / t1_E) * 100
  elif t2_E != 0:
     diff_E = t2_E
  else:
     diff_E = 0
  if t1_Pidle != 0:
    diff_Pidle = (abs(t1_Pidle - t2_Pidle) / t1_Pidle) * 100
  elif t2_Pidle != 0:
     diff_Pidle = t2_Pidle
  else:
     diff_Pidle = 0

  if simulator == "MM1K":
      if t1_Ploss != 0:
        diff_Ploss = (abs(t1_Ploss - t2_Ploss) / t1_Ploss) * 100
      elif t2_Ploss != 0:
         diff_Ploss = t2_Ploss
      else:
         diff_Ploss = 0
  print(f"Difference between simulations for {r} is E[n]: {diff_E}%, P(idle): {diff_Pidle}%, P(loss): {diff_Ploss}%")
