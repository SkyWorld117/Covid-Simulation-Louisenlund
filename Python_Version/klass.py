import random, math
from fixed_parameters import *

class Class:

    def __init__(self, num_students, num_teachers):
        self.warning = False
        self.num_students = num_students
        self.num_teachers = num_teachers

    def pick(self, crew):
        self.crew = [None, None]
        self.crew[0] = random.sample(crew[0], self.num_students)
        self.crew[1] = random.sample(crew[1], self.num_teachers)

    def in_class(self, position):
        if position[0]>=self.class_border[0][0] and position[0]<=self.class_border[1][0] and position[1]>=self.class_border[1][1] and position[1]<=self.class_border[0][1]:
            return True
        else:
            return False

    def lessoning(self, walls, fakewalls):
        self.class_border = ((walls[0][0][0],walls[0][1][1]), (walls[1][0][0],walls[1][1][0]))
        for i in self.crew:
            for j in i:
                if j.position==(None,None):
                    j.position = (random.uniform(d, lund_size[0]-d), random.uniform(cwh, lund_size[1]-hwh))
                if not self.in_class(j.position) and (j.destination==None or not self.in_class(j.destination)):
                    j.destination = (random.uniform(self.class_border[0][0]+d, self.class_border[1][0]-d), random.uniform(self.class_border[1][1]+d, self.class_border[0][1]-d))
                    j.step = move_speed
                elif self.in_class(j.position) and j.destination!=None and math.sqrt((j.destination[0]-j.position[0])**2+(j.destination[1]-j.position[1])**2)<j.step:
                    j.destination = None
                    j.step = indoor_speed
                elif self.in_class(j.position) and j.destination==None:
                    j.step = indoor_speed
                loc_1 = j.position[1]>lund_size[1]-hwh or j.position[1]<cwh
                j.move(fakewalls)
                loc_2 = j.position[1]>lund_size[1]-hwh or j.position[1]<cwh
                if loc_1!=loc_2:
                    if not loc_2 and (self.warning or random.choices([True, False], weights=(1-j.break_rules, j.break_rules), k=1)[0]):
                        j.radius = radius_with_masks
                    else:
                        j.radius = radius_without_masks
