module louisenlund
    using Random
    include("./fixed_parameters.jl")
    using .fixed_parameters
    include("./cohort.jl")
    using .cohort
    include("house.jl")
    using .house

    function get_num_ex_teachers(houses, class_info)
        num_ex_teachers = 0
        for info in class_info
            num_ex_teachers += info[2]
        end
        for house in houses
            num_ex_teachers -= length(house.crew[2])
        end
        return num_ex_teachers
    end

    function get_house_walls(index)
        if index==1
            return [([0,0], [lund_size[2]-hwh,lund_size[2]]), lundwalls[1]]
        elseif index==num_houses
            return [lundwalls[num_houses-1], ([lund_size[1],lund_size[1]], [lund_size[2]-hwh,lund_size[2]])]
        else
            return [lundwalls[index-1], lundwalls[index]]
        end
    end

    function get_classroom_walls(index)
        if index==1
            return [([0,0], [0,cwh]), lundwalls[num_houses]]
        elseif index==num_classrooms
            return [lundwalls[end], ([lund_size[1],lund_size[1]], [0,cwh])]
        else
            return [lundwalls[num_houses+index-2], lundwalls[num_houses+index-1]]
        end
    end

    function extend!(aTuple::Tuple)
        result = aTuple[1]
        for i in 2:length(aTuple)
            for j in aTuple[i]
                push!(result, j)
            end
        end
        return result
    end

    mutable struct Louisenlund
        intern_random_infection_rate::Float64
        extern_random_infection_rate::Float64
        teacher_break_rules::Float64
        student_break_rules::Float64
        num_cohorts::Int64

        cohorts::Array
        houses::Array
        classes::Array
        fakewalls::Array
        classrooms::Array
        chosen_classes::Array

        tick::Int64
        infected_list::Array
        healthy_list::Array
        regulation::Bool
        quarantine::Int64

        ticking::Any
        start_infection::Any

        function Louisenlund(num_cohorts::Int64, regulation::Bool, intern_random_infection_rate::Float64, extern_random_infection_rate::Float64, teacher_break_rules::Float64, student_break_rules::Float64)
            Weiden = House(get_house_walls(1), 16, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Kuh = House(get_house_walls(2), 16, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Meierei = House(get_house_walls(3), 20, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Allee = House(get_house_walls(4), 12, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Eschen = House(get_house_walls(5), 21, 2, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            House_E_9 = [Weiden, Kuh, Meierei, Allee, Eschen]
            class_info_E_9 = [(15,3), (10,2), (7,2), (15,3), (11,3), (8,2), (9,2), (15,3), (12,3)]
            num_ex_t_E_9 = get_num_ex_teachers(House_E_9, class_info_E_9)

            Fuchsbau_Q1 = House(get_house_walls(24), 4, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Förse_unten = House(get_house_walls(22), 14, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Ahorn = House(get_house_walls(15), 12, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Glocken = House(get_house_walls(10), 7, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Gärtnerei = House(get_house_walls(17), 6, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Eichen_oben = House(get_house_walls(18), 14, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Linden = House(get_house_walls(20), 17, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Förse_oben = House(get_house_walls(23), 21, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            House_Q1 = [Fuchsbau_Q1, Förse_unten, Ahorn, Glocken, Gärtnerei, Eichen_oben, Linden, Förse_oben]
            class_info_Q1 = [(12,3), (12,3), (16,3), (14,3), (17,3), (17,3), (7,2)]
            num_ex_t_Q1 = get_num_ex_teachers(House_Q1, class_info_Q1)

            Pibo = House(get_house_walls(16), 13, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Marstall = House(get_house_walls(8), 3, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Hausmeisterei = House(get_house_walls(7), 2, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Fuchsbau_Q2 = House(get_house_walls(25), 4, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Wald = House(get_house_walls(13), 11, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Buchen = House(get_house_walls(21), 7, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Gilden = House(get_house_walls(14), 16, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Schloss_rechts = House(get_house_walls(12), 7, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            House_Q2 = [Pibo, Marstall, Hausmeisterei, Fuchsbau_Q2, Wald, Buchen, Gilden, Schloss_rechts]
            class_info_Q2 = [(10,2), (17,3), (17,3), (8,2), (15,3)]
            num_ex_t_Q2 = get_num_ex_teachers(House_Q2, class_info_Q2)

            Birken = House(get_house_walls(6), 14, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Schloss_links = House(get_house_walls(11), 6, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Eichen_unten = House(get_house_walls(19), 11, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Fuchsbau_IB = House(get_house_walls(26), 4, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            Kava = House(get_house_walls(9), 23, 1, intern_random_infection_rate, student_break_rules, teacher_break_rules)
            House_IB = [Birken, Schloss_links, Eichen_unten, Fuchsbau_IB, Kava]
            class_info_IB = [(11,3), (29,6), (18,4)]
            num_ex_t_IB = get_num_ex_teachers(House_IB, class_info_IB)

            if num_cohorts==1
                my_cohorts = [Cohort(21, num_ex_t_E_9+num_ex_t_Q1+num_ex_t_Q2+num_ex_t_IB, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, extend!((House_E_9,House_Q1,House_Q2,House_IB)), extend!((class_info_E_9,class_info_Q1,class_info_Q2,class_info_IB)))]
            elseif num_cohorts==2
                E_9 = Cohort(17, num_ex_t_E_9, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_E_9, class_info_E_9)
                Q1_Q2_IB = Cohort(4, num_ex_t_Q1+num_ex_t_Q2+num_ex_t_IB, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, extend!((House_Q1,House_Q2,House_IB)), extend!((class_info_Q1,class_info_Q2,class_info_IB)))
                my_cohorts = [E_9, Q1_Q2_IB]
            elseif num_cohorts==3
                E_9 = Cohort(17, num_ex_t_E_9, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_E_9, class_info_E_9)
                Q1_Q2 = Cohort(4, num_ex_t_Q1+num_ex_t_Q2, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, extend!((House_Q1,House_Q2)), extend!((class_info_Q1,class_info_Q2)))
                IB = Cohort(0, num_ex_t_IB, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_IB, class_info_IB)
                my_cohorts = [E_9, Q1_Q2, IB]
            elseif num_cohorts==4
                E_9 = Cohort(17, num_ex_t_E_9, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_E_9, class_info_E_9)
                Q1 = Cohort(0, num_ex_t_Q1, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_Q1, class_info_Q1)
                Q2 = Cohort(4, num_ex_t_Q2, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_Q2, class_info_Q2)
                IB = Cohort(0, num_ex_t_IB, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, House_IB, class_info_IB)
                my_cohorts = [E_9, Q1, Q2, IB]
            end

            my_classes = Any[]
            my_houses = Any[]
            for i in my_cohorts
                my_classes = extend!((my_classes, i.classes))
                my_houses = extend!((my_houses, i.houses))
            end
            my_fakewalls = Tuple[]
            for i in my_cohorts
                for j in i.houses
                    for k in i.houses
                        if j!=k
                            for w in j.walls
                                if w in k.walls && !(w in my_fakewalls)
                                    push!(my_fakewalls, w)
                                end
                            end
                        end
                    end
                end
            end

            new(intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules, num_cohorts, my_cohorts, my_houses, my_classes, my_fakewalls, Vector(1:num_classrooms), Any[], 0, Any[], Any[], regulation, 0, ticking, start_infection)
        end
    end

    function ticking(self::Louisenlund, move_intensity::Int64, free_from_quarantine::Float64, time_of_lessons::Float64, num_lessons::Int64, time_in_house::Float64)
        self.tick += 1

        if self.tick%(day_tick/move_intensity)<time_of_lessons*day_tick/move_intensity
            if (self.tick%(day_tick/move_intensity))%(time_of_lessons/num_lessons*day_tick)==0
                empty!(self.chosen_classes)
            end
            if self.chosen_classes==[]
                Random.shuffle!(self.classrooms)
                Random.shuffle!(self.classes)
                self.chosen_classes = self.classes[1:20]
            end
            classrooms = deepcopy(self.classrooms)
            for i in self.cohorts
                if !self.regulation || (self.regulation && !i.quarantine)
                    for c in i.classes
                        if c in self.chosen_classes
                            #println(classrooms[end])
                            c.lessoning(c, get_classroom_walls(pop!(classrooms)), self.fakewalls)
                        else
                            for j in c.crew
                                for k in j
                                    if k.intern
                                        k.destination = nothing
                                        k.move(k, self.fakewalls)
                                        k.step = move_speed
                                    else
                                        k.position = (nothing, nothing)
                                    end
                                end
                            end
                        end
                    end
                else
                    i.house_time(i, self.fakewalls)
                end
            end
        else
            for i in self.cohorts
                i.house_time(i, self.fakewalls)
            end
            empty!(self.chosen_classes)
        end

        for (i, j, k) in self.infected_list
            for (a, b, c) in self.healthy_list
                if self.tick%infection_period==0 && !self.cohorts[i].crew[j][k].in_quarantine && self.cohorts[i].crew[j][k].position!=(nothing,nothing) && self.cohorts[a].crew[b][c].position!=(nothing,nothing) && self.cohorts[i].crew[j][k].contact(self.cohorts[i].crew[j][k], self.cohorts[a].crew[b][c])
                    push!(self.infected_list, (a, b, c))
                    filter!(e->e!=(a, b, c), self.healthy_list)
                end
            end

            self.cohorts[i].crew[j][k].infected_time += 1
            if self.cohorts[i].crew[j][k].in_quarantine
                self.cohorts[i].crew[j][k].quarantine_time += 1
            end

            if !self.cohorts[i].crew[j][k].show_infection_sign
                if self.regulation && self.tick%day_tick==0
                    show_infection_sign = get_show_infection_sign_rate(self.cohorts[i].crew[j][k].infected_time/day_tick)
                    self.cohorts[i].crew[j][k].show_infection_sign = rand()<=show_infection_sign ? true : false
                else
                    self.cohorts[i].crew[j][k].show_infection_sign = false
                end
            end
            if !self.cohorts[i].crew[j][k].in_quarantine && self.cohorts[i].crew[j][k].show_infection_sign && (rand()<=1-free_from_quarantine || self.cohorts[i].quarantine)
                self.cohorts[i].crew[j][k].in_quarantine = true
                self.quarantine += 1
                if self.regulation
                    self.cohorts[i].set_Quarantine(self.cohorts[i])
                    for z in self.cohorts
                        z.warn(z)
                    end
                end
            end

            if self.cohorts[i].crew[j][k].infected_time > end_infection_time*day_tick
                self.cohorts[i].crew[j][k].infected = false
                self.cohorts[i].crew[j][k].show_infection_sign = false
                if self.cohorts[i].crew[j][k].in_quarantine
                    self.quarantine -= 1
                    self.cohorts[i].crew[j][k].in_quarantine = false
                    cure_rate = get_cure_rate((self.cohorts[i].crew[j][k].infected_time-self.cohorts[i].crew[j][k].quarantine_time)/day_tick)
                    if rand() <= cure_rate
                        self.cohorts[i].crew[j][k].immunized = true
                    else
                        self.cohorts[i].crew[j][k].alive = false
                    end
                else
                    if !self.cohorts[i].crew[j][k].show_infection_sign || rand()<=1-death_rate
                        self.cohorts[i].crew[j][k].immunized = true
                    else
                        self.cohorts[i].crew[j][k].alive = false
                    end
                end
                filter!(e->e!=(i, j, k), self.infected_list)
            end
        end

        for (i, c) in enumerate(self.cohorts)
            if c.quarantine
                c.quarantine_time += 1
                if c.quarantine_time%day_tick==0
                    for (x, y, z) in self.infected_list
                        if x==i && !self.cohorts[x].crew[y][z].in_quarantine && rand()<=1-fake_negative_test
                            self.cohorts[x].crew[y][z].in_quarantine = true
                            self.quarantine += 1
                        end
                    end
                    c.quarantine = false
                    c.quarantine_time = 0
                    for h in c.houses
                        h.quarantine = false
                    end
                end
            end
        end
    end

    function start_infection(self::Louisenlund)
        i = rand(1:self.num_cohorts)
        j = rand(1:2)
        k = rand(1:length(self.cohorts[i].crew[j]))
        self.cohorts[i].crew[j][k].infected = true

        push!(self.infected_list, (i, j, k))
        for a in 1:self.num_cohorts
            for b in 1:2
                for c in 1:length(self.cohorts[a].crew[b])
                    if (a, b, c) != (i, j, k)
                        push!(self.healthy_list, (a, b, c))
                    end
                end
            end
        end
    end

    export Louisenlund

end
