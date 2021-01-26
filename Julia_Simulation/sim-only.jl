include("./fixed_parameters.jl")
using .fixed_parameters
include("./louisenlund.jl")
using .louisenlund

num_cohorts = 4
regulation = true
move_intensity = 1 # times per day (two-way trip)
#student_break_rules = 0.05 # percent
#teacher_break_rules = 0.01 # percent
free_from_quarantine = 0.05 # percent
time_of_lessons = 0.625 # percent
num_lessons = 10
time_in_house = 0.375 # percent
emergency_regulation = true
intern_random_infection_rate = 0.002
extern_random_infection_rate = 0.01

function simulation(student_break_rules, teacher_break_rules)
    LUND = Louisenlund(num_cohorts, regulation, intern_random_infection_rate, extern_random_infection_rate, teacher_break_rules, student_break_rules)
    LUND.start_infection(LUND)
    data = Array{Float32, 2}(undef, (6, sim_time*day_tick))
    end_infection = false
    while !end_infection
        healthy, dead, infected, immunized = 0, 0, 0, 0

        LUND.ticking(LUND, move_intensity, free_from_quarantine, time_of_lessons, num_lessons, time_in_house)

        for i in LUND.cohorts
            for j in i.crew
                for k in j
                    if k.infected && !k.in_quarantine
                        infected += 1
                    elseif !k.alive
                        dead += 1
                    elseif k.immunized
                        immunized += 1
                    elseif !k.infected
                        healthy += 1
                    end
                end
            end
        end

        data[1,LUND.tick] = Float32(LUND.tick/day_tick)
        data[2,LUND.tick] = Float32(healthy)
        data[3,LUND.tick] = Float32(infected)
        data[4,LUND.tick] = Float32(immunized)
        data[5,LUND.tick] = Float32(dead)
        data[6,LUND.tick] = Float32(LUND.quarantine)

        if LUND.tick%day_tick==0
            println("Day ", data[1,LUND.tick], " Healthy ", data[2,LUND.tick], " Infected ", data[3,LUND.tick], " Immunized ", data[4,LUND.tick], " Dead ", data[5,LUND.tick], " In quarantine ", data[6,LUND.tick])
        end

        if (length(LUND.infected_list)==0 && LUND.quarantine==0) || length(LUND.healthy_list)==0 || LUND.tick÷day_tick==sim_time || data[3,LUND.tick]==0
            end_infection = true
        end
    end

    return data[:,1:LUND.tick]
end

using HDF5
function save_Data(data, path::String)
    h5open(path, "w") do file
        write(file, "data", data)
    end
end

using .Threads
Threads.@threads for break_rules in 0.0:0.2:1.0
    save_Data(simulation(break_rules, break_rules), "./Data/default_c=4_5/break_rules="*string(break_rules)*".h5")
end
