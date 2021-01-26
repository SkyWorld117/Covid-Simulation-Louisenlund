import time
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
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
        healthy, dead, infected, immunized = [[], []], [[], []], [[], []], [[], []]
        start = time.time()
        LUND.ticking(move_intensity, free_from_quarantine, time_of_lessons, num_lessons, time_in_house)
        if (len(LUND.infected_list)==0 and LUND.quarantine==0) or len(LUND.healthy_list)==0:
            end_infection = True

        for i in LUND.cohorts:
            for j in i.crew:
                for k in j:
                    if k.infected and not k.in_quarantine:
                        for l in range(2):
                            infected[l].append(k.position[l])
                    elif not k.alive:
                        for l in range(2):
                            dead[l].append(k.position[l])
                    elif k.immunized:
                        for l in range(2):
                            immunized[l].append(k.position[l])
                    elif not k.infected:
                        for l in range(2):
                            healthy[l].append(k.position[l])

        data[0].append(LUND.tick/day_tick)
        data[1].append(len(healthy[0]))
        data[2].append(len(infected[0]))
        data[3].append(len(immunized[0]))
        data[4].append(len(dead[0]))
        data[5].append(LUND.quarantine)

        yield data, healthy, dead, infected, immunized, end_infection

sim = simulation()

fig, axes = plt.subplots(ncols=2, figsize=window_size, gridspec_kw={'width_ratios': width_ratios})
fig.canvas.set_window_title('Covid-19 Simulation')

axes[0].set_title('Simulation')
axes[0].axis('off')

for bound in lundbounds:
    axes[0].plot(bound[0], bound[1], color='black')
for wall in lundwalls:
    if not wall in LUND.fakewalls:
        axes[0].plot(wall[0], wall[1], color='black')
    else:
        axes[0].plot(wall[0], wall[1], color='grey', linestyle='--')

scs = []
scs.append(axes[0].scatter([], [], color='blue', s=5, animated=True))
scs.append(axes[0].scatter([], [], color='black', s=5, animated=True))
scs.append(axes[0].scatter([], [], color='red', s=5, animated=True))
scs.append(axes[0].scatter([], [], color='green', s=5, animated=True))

axes[1].set_title('Statistics')
axes[1].set_xlim(xmin=0, xmax=sim_time)
axes[1].set_ylim(ymin=0, ymax=400)
axes[1].set_xlabel('days')
axes[1].set_ylabel('persons')
data_labels = ['number of the healthy', 'number of the infected', 'number of the immunized', 'number of the dead', 'number of those in quarantine']
data_colors = ['blue', 'red', 'green', 'black', 'orange']
lines = []
for i in range(1, 6):
    lines.append(axes[1].plot([], [], color=data_colors[i-1], label=data_labels[i-1], animated=True)[0])
axes[1].legend(loc='upper right')

fig.show()
fig.canvas.draw()
backgrounds = [fig.canvas.copy_from_bbox(ax.bbox) for ax in axes]
tick = 0
end_simulation = False
while not end_simulation:
    tick += 1
    data, healthy, dead, infected, immunized, end_simulation = next(sim)
    print('\rDay %f: Healthy %d, Infected %d, Immunized %d, Dead %d, In quarantine %d' %(data[0][-1], data[1][-1], data[2][-1], data[3][-1], data[4][-1], data[5][-1]), end='')
    if tick%render_rate!=0:
        continue
    fig.canvas.restore_region(backgrounds[0])
    scs[0].set_offsets(np.c_[healthy[0], healthy[1]])
    scs[1].set_offsets(np.c_[dead[0], dead[1]])
    scs[2].set_offsets(np.c_[infected[0], infected[1]])
    scs[3].set_offsets(np.c_[immunized[0], immunized[1]])
    for i in range(4):
        axes[0].draw_artist(scs[i])
    fig.canvas.restore_region(backgrounds[1])
    for i in range(5):
        axes[1].text(data[0][-1]+0.5, data[i+1][-1], str(data[i+1][-1]))
        lines[i].set_data(data[0], data[i+1])
        axes[1].draw_artist(lines[i])
    fig.canvas.blit(axes[0].bbox)
    fig.canvas.blit(axes[1].bbox)
input()
