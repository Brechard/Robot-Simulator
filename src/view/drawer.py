import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

data_two_rooms = [[], []]
data_three_rooms = [[], [], []]

data_one_room = np.array(
    pd.read_csv("/Users/erytheis/PycharmProjects/Robot-Simulator/src/results/0311_041755room1.csv"))

data_two_rooms[0] = np.array(
    pd.read_csv("/Users/erytheis/PycharmProjects/Robot-Simulator/src/results/0310_133314room1.csv"))
data_two_rooms[1] = np.array(
    pd.read_csv("/Users/erytheis/PycharmProjects/Robot-Simulator/src/results/0310_133314room2.csv"))

data_three_rooms = np.array(
    pd.read_csv("/Users/erytheis/PycharmProjects/Robot-Simulator/src/results/0312_002820room1.csv"))




data_two_rooms = (np.array(data_two_rooms[0]) + np.array(data_two_rooms[1])) / 2



one_room_max = np.zeros(data_one_room.shape[0])
two_room_max = np.zeros(data_one_room.shape[0])
three_room_max = np.zeros(data_one_room.shape[0])
one_room_std = np.zeros(data_one_room.shape[0])
two_room_std = np.zeros(data_one_room.shape[0])
three_room_std = np.zeros(data_one_room.shape[0])
one_room_avg = np.zeros(data_one_room.shape[0])
two_room_avg = np.zeros(data_one_room.shape[0])
three_room_avg = np.zeros(data_one_room.shape[0])

for i in range(len(data_two_rooms)):
    one_room_max[i] = np.max(data_one_room[i])
    two_room_max[i] = np.max(data_two_rooms[i])
    three_room_max[i] = np.max(data_three_rooms[i])
    one_room_avg[i] = np.mean(data_one_room[i])
    two_room_avg[i] = np.mean(data_two_rooms[i])
    three_room_avg[i] = np.mean(data_three_rooms[i])
    one_room_std[i] = np.std(data_one_room[i])
    two_room_std[i] = np.std(data_two_rooms[i])

plt.figure(1)
plt.plot(range(49), one_room_avg, 'or')
plt.plot(range(49), two_room_avg, 'ob')
plt.plot(range(49), three_room_avg, 'og')
plt.plot(range(49), one_room_avg, '-', color = 'red')
plt.plot(range(49), two_room_avg, '-', color = 'blue')
plt.plot(range(49), three_room_avg, '-', color = 'green')


# plt.fill_between(range(49), one_room_avg - one_room_std, one_room_avg + one_room_std,
#                  color = 'red', alpha = 0.2)
# plt.fill_between(range(49), two_room_avg - two_room_std, two_room_avg + two_room_std,
#                  color = 'blue', alpha = 0.2)
plt.xlim(0, 50)
plt.xlabel("Generation")
plt.title("Average fitness")
plt.gca().legend(('one room','two rooms', 'three rooms'))

plt.figure(2)
plt.plot(range(49), one_room_max, 'or')
plt.plot(range(49), two_room_max, 'ob')
plt.plot(range(49), three_room_max, 'og')
plt.plot(range(49), one_room_max, '-', color = 'red')
plt.plot(range(49), two_room_max, '-', color = 'blue')
plt.plot(range(49), three_room_max, '-', color = 'green')
plt.gca().legend(('one room','two rooms', 'three rooms'))
# plt.fill_between(range(49), one_room_max - one_room_std, one_room_max + one_room_std,
#                  color = 'red', alpha = 0.2)
# plt.fill_between(range(49), two_room_max - two_room_std, two_room_max + two_room_std,
#                  color = 'blue', alpha = 0.2)
plt.xlim(0, 50)
plt.xlabel("Generation")
plt.title("Maximum fitness")
plt.show()

# data = np.transpose(data)


# fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))
# idx = [0, 10 ,30]
#
# for i in range(3):
#
#         ax = axes[i]
#         n, bins, patches = ax.hist(x = data[idx[i]],weights=np.ones(len(data[idx[i]])) / len(data[idx[i]]),  bins = 15,
#                                     alpha = 0.7, rwidth = 0.90)
#         ax.set_xlabel('Fitness')
#         ax.set_ylabel('Generation '+str(idx[i]))
#         leg = ax.legend(loc='upper left')
#         leg.draw_frame(False)
#
# axes[0].set_title('Distribution of fitness', fontweight='bold')
# plt.show()
