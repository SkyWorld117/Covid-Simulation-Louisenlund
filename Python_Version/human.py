from fixed_parameters import *
import random, math

class Human:

    def __init__(self, spawnpoint, break_rules, intern, random_infection_rate):
        self.radius = radius_without_masks
        self.position = spawnpoint
        self.intern = intern
        self.random_infection_rate = random_infection_rate
        self.infected = False
        self.infected_time = 0 # tick
        self.show_infection_sign = False
        self.in_quarantine = False
        self.quarantine_time = 0 # tick
        self.immunized = False
        self.alive = True
        self.destination = None
        self.step = move_speed
        self.break_rules = break_rules

    def contact(self, human):
        distance = math.sqrt((self.position[0]-human.position[0])**2+(self.position[1]-human.position[1])**2)
        if distance>=radius_without_masks:
            return False
        infection_distance = get_infection_distance(self.radius, human.radius)
        if distance < infection_distance:
            infection_rate = get_infection_rate(distance, infection_distance)
            infection_active_rate = get_infection_active_rate(self.infected_time/day_tick)
            if random.choices([True, False], weights=(infection_rate*infection_active_rate, 1-infection_rate*infection_active_rate), k=1)[0]:
                human.infected = True
                return True
        return False

    def get_override_permission(self, fakewalls):
        for wall in lundwalls:
            if not wall in fakewalls and wall[0][0]>min(self.position[0], self.destination[0]) and wall[0][0]<max(self.position[0], self.destination[0]):
                height = ((self.destination[1]-self.position[1])/(self.destination[0]-self.position[0]))*(wall[0][0]-self.position[0])+self.position[1]
                if height>=wall[1][0] and height<=wall[1][1]:
                    return True
        return False

    def move(self, fakewalls):
        if not self.alive or self.in_quarantine:
            return None
        if self.destination==None or random.choices([True, False], weights=(move_random_rate, 1-move_random_rate), k=1)[0]:
            angle = random.randint(0, 360)
            x = math.cos(angle)*self.step
            y = math.sin(angle)*self.step
        else:
            destination_override = self.get_override_permission(fakewalls)
            if destination_override:
                temp = self.destination
                if self.position[1]<=cwh or self.position[1]>=lund_size[1]-hwh:
                    self.destination = (self.position[0], random.uniform(cwh, lund_size[1]-hwh))
                else:
                    self.destination = (self.destination[0], random.uniform(cwh, lund_size[1]-hwh))
            length_x = self.destination[0]-self.position[0]
            length_y = self.destination[1]-self.position[1]
            x = (self.step*length_x)/math.sqrt(length_x**2+length_y**2)
            y = (self.step*length_y)/math.sqrt(length_x**2+length_y**2)
            if destination_override:
                self.destination = temp
        new_position = [self.position[0]+x, self.position[1]+y]

        for wall in lundwalls:
            if not wall in fakewalls and wall[0][0]<max(new_position[0], self.position[0]) and wall[0][0]>min(new_position[0], self.position[0]):
                height = (y*(wall[0][0]-self.position[0]))/x+self.position[1]
                if height>=wall[1][0] and height<=wall[1][1]:
                    new_position[0] = wall[0][0]-(x/abs(x))*d
                break
        for i in range(2):
            if new_position[i] < d:
                new_position[i] = d
            elif new_position[i] > lund_size[i]-d:
                new_position[i] = lund_size[i]-d
        for wall in lundwalls:
            if not wall in fakewalls and abs(new_position[0]-wall[0][0]) < d:
                new_position[0] = wall[0][0]+((new_position[0]-wall[0][0])*d)/abs(new_position[0]-wall[0][0])
        self.position = tuple(new_position)
