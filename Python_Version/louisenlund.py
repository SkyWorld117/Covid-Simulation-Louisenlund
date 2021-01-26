import random, time, copy
from fixed_parameters import *
from cohort import Cohort
from house import House

class Louisenlund:

    def __init__(self, num_cohorts, regulation, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules):
        self.intern_random_infection_rate = intern_random_infection_rate
        self.extern_random_infection_rate = extern_random_infection_rate
        self.teacher_break_rules = teacher_break_rules
        self.student_break_rules = student_break_rules

        self.num_cohorts = num_cohorts

        Weiden = House(self.get_house_walls(1), 16, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Kuh = House(self.get_house_walls(2), 16, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Meierei = House(self.get_house_walls(3), 20, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Allee = House(self.get_house_walls(4), 12, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Eschen = House(self.get_house_walls(5), 21, 2, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        House_E_9 = [Weiden, Kuh, Meierei, Allee, Eschen]
        class_info_E_9 = [(15,3), (10,2), (7,2), (15,3), (11,3), (8,2), (9,2), (15,3), (12,3)]
        num_ex_t_E_9 = self.get_num_ex_teachers(House_E_9, class_info_E_9)

        Fuchsbau_Q1 = House(self.get_house_walls(24), 4, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Förse_unten = House(self.get_house_walls(22), 14, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Ahorn = House(self.get_house_walls(15), 12, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Glocken = House(self.get_house_walls(10), 7, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Gärtnerei = House(self.get_house_walls(17), 6, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Eichen_oben = House(self.get_house_walls(18), 14, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Linden = House(self.get_house_walls(20), 17, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Förse_oben = House(self.get_house_walls(23), 21, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        House_Q1 = [Fuchsbau_Q1, Förse_unten, Ahorn, Glocken, Gärtnerei, Eichen_oben, Linden, Förse_oben]
        class_info_Q1 = [(12,3), (12,3), (16,3), (14,3), (17,3), (17,3), (7,2)]
        num_ex_t_Q1 = self.get_num_ex_teachers(House_Q1, class_info_Q1)

        Pibo = House(self.get_house_walls(16), 13, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Marstall = House(self.get_house_walls(8), 3, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Hausmeisterei = House(self.get_house_walls(7), 2, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Fuchsbau_Q2 = House(self.get_house_walls(25), 4, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Wald = House(self.get_house_walls(13), 11, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Buchen = House(self.get_house_walls(21), 7, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Gilden = House(self.get_house_walls(14), 16, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Schloss_rechts = House(self.get_house_walls(12), 7, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        House_Q2 = [Pibo, Marstall, Hausmeisterei, Fuchsbau_Q2, Wald, Buchen, Gilden, Schloss_rechts]
        class_info_Q2 = [(10,2), (17,3), (17,3), (8,2), (15,3)]
        num_ex_t_Q2 = self.get_num_ex_teachers(House_Q2, class_info_Q2)

        Birken = House(self.get_house_walls(6), 14, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Schloss_links = House(self.get_house_walls(11), 6, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Eichen_unten = House(self.get_house_walls(19), 11, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Fuchsbau_IB = House(self.get_house_walls(26), 4, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        Kava = House(self.get_house_walls(9), 23, 1, self.intern_random_infection_rate, self.student_break_rules, self.teacher_break_rules)
        House_IB = [Birken, Schloss_links, Eichen_unten, Fuchsbau_IB, Kava]
        class_info_IB = [(11,3), (29,6), (18,4)]
        num_ex_t_IB = self.get_num_ex_teachers(House_IB, class_info_IB)

        if num_cohorts==1:
            self.cohorts = [Cohort(21, num_ex_t_E_9+num_ex_t_Q1+num_ex_t_Q2+num_ex_t_IB, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_E_9+House_Q1+House_Q2+House_IB, class_info_E_9+class_info_Q1+class_info_Q2+class_info_IB)]
        elif num_cohorts==2:
            E_9 = Cohort(17, num_ex_t_E_9, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_E_9, class_info_E_9)
            Q1_Q2_IB = Cohort(4, num_ex_t_Q1+num_ex_t_Q2+num_ex_t_IB, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_Q1+House_Q2+House_IB, class_info_Q1+class_info_Q2+class_info_IB)
            self.cohorts = [E_9, Q1_Q2_IB]
        elif num_cohorts==3:
            E_9 = Cohort(17, num_ex_t_E_9, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_E_9, class_info_E_9)
            Q1_Q2 = Cohort(4, num_ex_t_Q1+num_ex_t_Q2, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_Q1+House_Q2, class_info_Q1+class_info_Q2)
            IB = Cohort(0, num_ex_t_IB, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_IB, class_info_IB)
            self.cohorts = [E_9, Q1_Q2, IB]
        elif num_cohorts==4:
            E_9 = Cohort(17, num_ex_t_E_9, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_E_9, class_info_E_9)
            Q1 = Cohort(0, num_ex_t_Q1, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_Q1, class_info_Q1)
            Q2 = Cohort(4, num_ex_t_Q2, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_Q2, class_info_Q2)
            IB = Cohort(0, num_ex_t_IB, self.intern_random_infection_rate, self.extern_random_infection_rate, self.teacher_break_rules, self.student_break_rules, House_IB, class_info_IB)
            self.cohorts = [E_9, Q1, Q2, IB]

        self.classes = []
        self.houses = []
        for i in self.cohorts:
            self.classes.extend(i.classes)
            self.houses.extend(i.houses)
        self.fakewalls = []
        for i in self.cohorts:
            for j in i.houses:
                for k in i.houses:
                    if j!=k:
                        for w in j.walls:
                            if w in k.walls and not w in self.fakewalls:
                                self.fakewalls.append(w)

        self.classrooms = list(range(1,num_classrooms+1))
        self.chosen_classes=[]

        self.tick = 0
        self.infected_list = []
        self.healthy_list = []
        self.regulation = regulation
        self.quarantine = 0

    def get_num_ex_teachers(self, houses, class_info):
        num_ex_teachers = 0
        for info in class_info:
            num_ex_teachers += info[1]
        for house in houses:
            num_ex_teachers -= len(house.crew[1])
        return num_ex_teachers

    def get_house_walls(self, index):
        if index==1:
            return [([0,0], [lund_size[1]-hwh,lund_size[1]]), lundwalls[0]]
        elif index==num_houses:
            return [lundwalls[num_houses-2], ([lund_size[0],lund_size[0]], [lund_size[1]-hwh,lund_size[1]])]
        else:
            return [lundwalls[index-2], lundwalls[index-1]]

    def get_classroom_walls(self, index):
        if index==1:
            return [([0,0], [0,cwh]), lundwalls[num_houses+index-2]]
        elif index==num_classrooms:
            return [lundwalls[-1], ([lund_size[0],lund_size[0]], [0,cwh])]
        else:
            return [lundwalls[num_houses+index-3], lundwalls[num_houses+index-2]]

    def ticking(self, move_intensity, free_from_quarantine, time_of_lessons, num_lessons, time_in_house):
        self.tick += 1

        if self.tick%(day_tick/move_intensity)<time_of_lessons*day_tick/move_intensity:
            if (self.tick%(day_tick/move_intensity))%(time_of_lessons/num_lessons*day_tick)==0:
                self.chosen_classes=[]
            if self.chosen_classes==[]:
                random.shuffle(self.classrooms)
                self.chosen_classes = random.sample(self.classes, 20)
            classrooms = copy.deepcopy(self.classrooms)
            for i in self.cohorts:
                if not self.regulation or (self.regulation and not i.quarantine):
                    for c in i.classes:
                        if c in self.chosen_classes:
                            c.lessoning(self.get_classroom_walls(classrooms.pop(0)), self.fakewalls)
                        else:
                            for j in c.crew:
                                for k in j:
                                    if k.intern:
                                        k.destination = None
                                        k.move(self.fakewalls)
                                        k.step = move_speed
                                    else:
                                        k.position = (None,None)
                else:
                    i.house_time(self.fakewalls)
        else:
            for i in self.cohorts:
                i.house_time(self.fakewalls)
            self.chosen_classes = []

        for i, j, k in self.infected_list:
            for a, b, c in self.healthy_list:
                if self.tick%infection_period==0 and not self.cohorts[i].crew[j][k].in_quarantine and self.cohorts[i].crew[j][k].position!=(None,None) and self.cohorts[a].crew[b][c].position!=(None,None) and self.cohorts[i].crew[j][k].contact(self.cohorts[a].crew[b][c]):
                    self.infected_list.append([a, b, c])
                    self.healthy_list.remove([a, b, c])

            self.cohorts[i].crew[j][k].infected_time += 1
            if self.cohorts[i].crew[j][k].in_quarantine:
                self.cohorts[i].crew[j][k].quarantine_time += 1

            if not self.cohorts[i].crew[j][k].show_infection_sign:
                if self.regulation and self.tick%day_tick==0:
                    show_infection_sign_rate = get_show_infection_sign_rate(self.cohorts[i].crew[j][k].infected_time/day_tick)
                    self.cohorts[i].crew[j][k].show_infection_sign = random.choices([True, False], weights=(show_infection_sign_rate, 1-show_infection_sign_rate), k=1)[0]
                else:
                    self.cohorts[i].crew[j][k].show_infection_sign = False
            if not self.cohorts[i].crew[j][k].in_quarantine and self.cohorts[i].crew[j][k].show_infection_sign and (random.choices([True, False], weights=(1-free_from_quarantine, free_from_quarantine), k=1)[0] or self.cohorts[i].quarantine):
                self.cohorts[i].crew[j][k].in_quarantine = True
                self.quarantine += 1
                if self.regulation:
                    self.cohorts[i].set_Quarantine()
                    for z in self.cohorts:
                        z.warn()

            if self.cohorts[i].crew[j][k].infected_time > end_infection_time*day_tick:
                self.cohorts[i].crew[j][k].infected = False
                self.cohorts[i].crew[j][k].show_infection_sign = False
                if self.cohorts[i].crew[j][k].in_quarantine:
                    self.quarantine -= 1
                    self.cohorts[i].crew[j][k].in_quarantine = False
                    cure_rate = get_cure_rate((self.cohorts[i].crew[j][k].infected_time-self.cohorts[i].crew[j][k].quarantine_time)/day_tick)
                    if random.choices([True, False], weights=(cure_rate, 1-cure_rate), k=1)[0]:
                        self.cohorts[i].crew[j][k].immunized = True
                    else:
                        self.cohorts[i].crew[j][k].alive = False
                else:
                    if random.choices([True, False], weights=(death_rate, 1-death_rate), k=1)[0]:
                        self.cohorts[i].crew[j][k].alive = False
                    else:
                        self.cohorts[i].crew[j][k].immunized = True
                self.infected_list.remove([i, j, k])

        for i,c in enumerate(self.cohorts):
            if c.quarantine:
                c.quarantine_time += 1
                if c.quarantine_time%day_tick==0:
                    for x,y,z in self.infected_list:
                        if x==i and not self.cohorts[x].crew[y][z].in_quarantine:
                            self.cohorts[x].crew[y][z].in_quarantine = random.choices([True, False], weights=(1-fake_negative_test, fake_negative_test), k=1)[0]
                    c.quarantine = False
                    c.quarantine_time = 0
                    for h in c.houses:
                        h.quarantine = False

    def start_infection(self):
        i = random.randint(0, self.num_cohorts-1)
        j = random.choice([0,1])
        k = random.randint(0, len(self.cohorts[i].crew[j])-1)
        self.cohorts[i].crew[j][k].infected = True

        self.infected_list.append([i, j, k])
        for a in range(self.num_cohorts):
            for b in range(2):
                for c in range(len(self.cohorts[a].crew[b])):
                    if (a, b, c) != (i, j, k):
                        self.healthy_list.append([a, b, c])
