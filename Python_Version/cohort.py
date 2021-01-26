import random, math, copy
from fixed_parameters import *
from human import Human
from klass import Class

class Cohort:

    def __init__(self, num_ex_students, num_ex_teachers, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, houses, class_info):
        self.quarantine = False
        self.warning = False
        self.quarantine_time = 0

        self.crew = [[], []]
        for i in range(num_ex_students):
            spawnpoint = (random.uniform(d, lund_size[0]-d), random.uniform(cwh, lund_size[1]-hwh))
            self.crew[0].append(Human(spawnpoint, student_break_rules, False, extern_random_infection_rate))
        for i in range(num_ex_teachers):
            spawnpoint = (random.uniform(d, lund_size[0]-d), random.uniform(cwh, lund_size[1]-hwh))
            self.crew[1].append(Human(spawnpoint, teacher_break_rules, False, extern_random_infection_rate))

        self.houses = houses
        for i in self.houses:
            self.crew[0].extend(i.crew[0])
            self.crew[1].extend(i.crew[1])

        self.classes = []
        for info in class_info:
            self.classes.append(Class(info[0], info[1]))
            self.classes[-1].pick(self.crew)
            for i in self.classes[-1].crew[0]:
                self.crew[0].remove(i)
            for i in self.classes[-1].crew[1]:
                self.crew[1].remove(i)
        for i in self.classes:
            self.crew[0].extend(i.crew[0])
            self.crew[1].extend(i.crew[1])

    def house_time(self, fakewalls):
        for i in self.houses:
            i.house_time(fakewalls)
        for i in self.crew:
            for j in i:
                if not j.intern:
                    j.position = (None,None)

    def lessoning(self, walls, fakewalls):
        for i in self.crew:
            for j in i:
                if not j.intern:
                    j.position = (random.uniform(d, lund_size[0]-d), random.uniform(cwh, lund_size[1]-hwh))
        for i,c in enumerate(self.classes):
            c.lessoning(walls[i*2:i*2+1], fakewalls)

    def set_Quarantine(self):
        self.quarantine = True
        for i in self.houses:
            i.quarantine = True

    def warn(self):
        self.warning = True
        for i in self.houses:
            i.warning = True
        for i in self.classes:
            i.warning = True
