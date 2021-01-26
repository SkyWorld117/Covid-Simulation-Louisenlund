module cohort
    using Random
    include("./fixed_parameters.jl")
    using .fixed_parameters
    include("./human.jl")
    using .human
    include("./class.jl")
    using .class

    mutable struct Cohort
        quarantine::Bool
        warning::Bool
        quarantine_time::Int64
        crew::Array
        houses::Array
        classes::Array

        house_time::Any
        set_Quarantine::Any
        warn::Any

        function Cohort(num_ex_students::Int64, num_ex_teachers::Int64, intern_random_infection_rate::Float64, extern_random_infection_rate::Float64, teacher_break_rules::Float64, student_break_rules::Float64, houses::Array, class_info::Array)
            my_crew = [Array{Any}(undef, num_ex_students), Array{Any}(undef, num_ex_teachers)]
            for i in 1:num_ex_students
                spawnpoint = (rand(d:0.01:lund_size[1]-d), rand(cwh:0.01:lund_size[2]-hwh))
                my_crew[1][i] = Human(spawnpoint, student_break_rules, false, extern_random_infection_rate)
            end
            for i in 1:num_ex_teachers
                spawnpoint = (rand(d:0.01:lund_size[1]-d), rand(cwh:0.01:lund_size[2]-hwh))
                my_crew[2][i] = Human(spawnpoint, teacher_break_rules, false, extern_random_infection_rate)
            end

            for i in houses
                for j in 1:2
                    for k in i.crew[j]
                        push!(my_crew[j], k)
                    end
                end
            end

            my_classes = Array{Any}(undef, length(class_info))
            Random.shuffle!(my_crew[1])
            Random.shuffle!(my_crew[2])
            start = [0,0]
            for (index, info) in enumerate(class_info)
                my_classes[index] = Class(info[1], info[2])
                my_classes[index].pick(my_classes[index], my_crew, start)
                start[1] += my_classes[index].num_students
                start[2] += my_classes[index].num_teachers
            end

            new(false, false, 0, my_crew, houses, my_classes, house_time, set_Quarantine, warn)
        end
    end

    function house_time(self::Cohort, fakewalls::Array)
        for i in self.houses
            i.house_time(i, fakewalls)
        end
        for i in self.crew
            for j in i
                if !j.intern
                    j.position = (nothing, nothing)
                end
            end
        end
    end

    function set_Quarantine(self::Cohort)
        self.quarantine = true
        for i in self.houses
            i.quarantine = true
        end
    end

    function warn(self::Cohort)
        self.warning = true
        for i in self.houses
            i.warning = true
        end
        for i in self.classes
            i.warning = true
        end
    end

    export Cohort

end
