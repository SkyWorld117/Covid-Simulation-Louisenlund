import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from louisenlund import Louisenlund
from fixed_parameters import *

regulation = True
move_intensity = 1 # times per day (two-way trip)
student_break_rules = 0.05 # percent
teacher_break_rules = 0.01 # percent
free_from_quarantine = 0.05 # percent
time_of_lessons = 0.625 # percent
num_lessons = 10
time_in_house = 0.375 # percent
emergency_regulation = True
intern_random_infection_rate = 0.002
extern_random_infection_rate = 0.01


LUND = Louisenlund(4, regulation, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules)
def simulation():
    global LUND
    LUND.start_infection()
    data = [[], [], [], [], [], []]
    end_infection = False
    while not end_infection:
        healthy, dead, infected, immunized = 0, 0, 0, 0
        #start = time.time()
        LUND.ticking(move_intensity, free_from_quarantine, time_of_lessons, num_lessons, time_in_house)
        #print('Simulation time usage: %f s' %(time.time()-start))
        if (len(LUND.infected_list)==0 and LUND.quarantine==0) or len(LUND.healthy_list)==0:
            end_infection = True

        for i in LUND.cohorts:
            for j in i.crew:
                for k in j:
                    if k.infected and not k.in_quarantine:
                        infected += 1
                    elif not k.alive:
                        dead += 1
                    elif k.immunized:
                        immunized += 1
                    elif not k.infected:
                        healthy += 1

        data[0].append(LUND.tick/day_tick)
        data[1].append(healthy)
        data[2].append(infected)
        data[3].append(immunized)
        data[4].append(dead)
        data[5].append(LUND.quarantine)

        yield data, end_infection

sim = simulation()
end_simulation = False
while not end_simulation:
    data, end_simulation = next(sim)
    print('\rDay %f: Healthy %d, Infected %d, Immunized %d, Dead %d, In quarantine %d' %(data[0][-1], data[1][-1], data[2][-1], data[3][-1], data[4][-1], data[5][-1]), end='')

fig = plt.figure(figsize=window_size)
fig.canvas.set_window_title('Covid-19 Simulation -- Chaos Gilde')
plt.xlabel('days')
plt.ylabel('persons')
data_labels = ['number of the healthy', 'number of the infected', 'number of the immunized', 'number of the dead', 'number of those in quarantine']
data_colors = ['blue', 'red', 'green', 'black', 'orange']
for i in range(1, 6):
    plt.plot(data[0], data[i], color=data_colors[i-1], label=data_labels[i-1])
fig.legend(loc='upper right')
fig.show()
input()
