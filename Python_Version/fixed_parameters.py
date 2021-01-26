from math import exp, log

tick_second_rate = 1 # tick/second
coord_meter_rate = 1 # pixel/meter


'''Basic'''
render_rate = 10
window_size = (16, 7) # inch
width_ratios = [5, 2]

radius_with_masks = 0.4*coord_meter_rate # pixel
radius_without_masks = 1.5*coord_meter_rate # pixel

move_random_rate = 0.2 # percent
move_speed = (coord_meter_rate*1.5)/tick_second_rate # pixel/tick
indoor_speed = (coord_meter_rate*0.5)/tick_second_rate # pixel/tick
quarantine_speed = (coord_meter_rate*0.2)/tick_second_rate # pixel/tick

day_tick = 86400*tick_second_rate#/128 # ticks
sim_time = 20 # days

end_infection_time = 14 # days
death_rate = 0.80 # percent
fake_negative_test = 0.04 # percent

'''Advanced'''
infection_period = 60 # tick
d = radius_without_masks/2

day_time = 60 # seconds in reality

lund_size = (400, 90)
cwh, hwh = 10, 10 # classroom wall height, house wall height
lundbounds = []
lundbounds.append(([0,lund_size[0]], [lund_size[1],lund_size[1]]))
lundbounds.append(([0,lund_size[0]], [0,0]))
lundbounds.append(([0,0], [0,lund_size[1]]))
lundbounds.append(([lund_size[0],lund_size[0]], [0,lund_size[1]]))

num_in = [16,16,20,12,21,14,2,3,23,7,6,7,11,16,12,13,6,14,11,17,7,14,21,4,4,4]
num_intern_students = 301
num_houses = len(num_in)
lundwalls = []
start = 0
for i in num_in[:-1]:
    start += i/num_intern_students*lund_size[0]
    lundwalls.append((2*[start], [lund_size[1]-hwh,lund_size[1]]))# Walls between houses
num_classrooms = 30
start = 0
for i in range(1, num_classrooms):
    start += 1/num_classrooms*lund_size[0]
    lundwalls.append((2*[start], [0,cwh]))# Walls between classrooms

def get_infection_distance(radius_1, radius_2):
    return max(radius_1, radius_2)-abs((radius_1-radius_2)/2)

def get_infection_rate(distance, infection_distance):
    return (0.95/infection_distance)*((infection_distance-distance)/(distance+1))

def get_show_infection_sign_rate(days):
    return 0.00156566*days**3-0.0493434*days**2+0.383939*days

def get_infection_active_rate(days):
    return exp((days-5.7)/1.1)/(exp((days-5.7)/1.1)+1)

def get_cure_rate(days):
    return log(end_infection_time-days+1)/log(end_infection_time+1)
