import random, math
from fixed_parameters import *
from human import Human

class House:

    def __init__(self, walls, number_of_students, number_of_teachers, intern_random_infection_rate, student_break_rules, teacher_break_rules):
        self.quarantine = False
        self.warning = False

        self.walls = walls
        self.house_border = ((self.walls[0][0][0],self.walls[0][1][1]), (self.walls[1][0][0],self.walls[1][1][0]))

        self.crew = [[],[]]
        for i in range(number_of_students):
            spawnpoint = (random.uniform(self.house_border[0][0]+d, self.house_border[1][0]-d), random.uniform(self.house_border[1][1]+d, self.house_border[0][1]-d))
            self.crew[0].append(Human(spawnpoint, student_break_rules, True, intern_random_infection_rate))
        for i in range(number_of_teachers):
            spawnpoint = (random.uniform(self.house_border[0][0]+d, self.house_border[1][0]-d), random.uniform(self.house_border[1][1]+d, self.house_border[0][1]-d))
            self.crew[1].append(Human(spawnpoint, teacher_break_rules, True, intern_random_infection_rate))

    def in_house(self, position):
        if position[0]>=self.house_border[0][0] and position[0]<=self.house_border[1][0] and position[1]>=self.house_border[1][1] and position[1]<=self.house_border[0][1]:
            return True
        else:
            return False

    def house_time(self, fakewalls):
        for i in self.crew:
            for j in i:
                if not self.in_house(j.position) and (j.destination==None or not self.in_house(j.destination)):
                    j.destination = (random.uniform(self.house_border[0][0]+d, self.house_border[1][0]-d), random.uniform(self.house_border[1][1]+d, self.house_border[0][1]-d))
                    j.step = move_speed
                elif self.in_house(j.position) and j.destination!=None and math.sqrt((j.destination[0]-j.position[0])**2+(j.destination[1]-j.position[1])**2)<j.step:
                    j.destination = None
                    j.step = indoor_speed
                elif self.in_house(j.position) and j.destination==None:
                    j.step = indoor_speed
                    if self.quarantine:
                        j.step = quarantine_speed
                loc_1 = j.position[1]>lund_size[1]-hwh or j.position[1]<cwh
                j.move(fakewalls)
                loc_2 = j.position[1]>lund_size[1]-hwh or j.position[1]<cwh
                if loc_1!=loc_2:
                    if not loc_2 and (self.warning or random.choices([True, False], weights=(1-j.break_rules, j.break_rules), k=1)[0]):
                        j.radius = radius_with_masks
                    else:
                        j.radius = radius_without_masks
