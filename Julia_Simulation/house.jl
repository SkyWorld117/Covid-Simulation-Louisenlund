module house
    include("./fixed_parameters.jl")
    using .fixed_parameters
    include("./human.jl")
    using .human

    mutable struct House
        quarantine::Bool
        warning::Bool
        walls::Array
        house_border::Tuple
        crew::Array

        in_house::Any
        house_time::Any

        function House(walls::Array, number_of_students::Int64, number_of_teachers::Int64, intern_random_infection_rate::Float64, student_break_rules::Float64, teacher_break_rules::Float64)
            house_border = ((walls[1][1][1],walls[1][2][2]), (walls[2][1][1],walls[2][2][1]))
            crew = [Array{Any}(undef, number_of_students), Array{Any}(undef, number_of_teachers)]
            for i in 1:number_of_students
                spawnpoint = (rand(house_border[1][1]+d:0.01:house_border[2][1]-d), rand(house_border[2][2]+d:0.01:house_border[1][2]-d))
                crew[1][i] = Human(spawnpoint, student_break_rules, true, intern_random_infection_rate)
            end
            for i in 1:number_of_teachers
                spawnpoint = (rand(house_border[1][1]+d:0.01:house_border[2][1]-d), rand(house_border[2][2]+d:0.01:house_border[1][2]-d))
                crew[2][i] = Human(spawnpoint, teacher_break_rules, true, intern_random_infection_rate)
            end

            new(false, false, walls, house_border, crew, in_house, house_time)
        end
    end

    function in_house(self::House, position::Tuple)
        if position[1]>=self.house_border[1][1] && position[1]<=self.house_border[2][1] && position[2]>=self.house_border[2][2] && position[2]<=self.house_border[1][2]
            return true
        else
            return false
        end
    end

    function house_time(self::House, fakewalls::Array)
        for i in self.crew
            for j in i
                if !self.in_house(self, j.position) && (j.destination==nothing || !self.in_house(self, j.destination))
                    j.destination = (rand(self.house_border[1][1]+d:0.01:self.house_border[2][1]-d), rand(self.house_border[2][2]+d:0.01:self.house_border[1][2]-d))
                    j.step = move_speed
                elseif self.in_house(self, j.position) && j.destination!=nothing && sqrt((j.destination[1]-j.position[1])^2+(j.destination[2]-j.position[2])^2)<j.step
                    j.destination = nothing
                    j.step = indoor_speed
                elseif self.in_house(self, j.position) && j.destination==nothing
                    j.step = indoor_speed
                    if self.quarantine
                        j.step = quarantine_speed
                    end
                end
                loc_1 = j.position[2]>lund_size[2]-hwh || j.position[2]<cwh
                j.move(j, fakewalls)
                loc_2 = j.position[2]>lund_size[2]-hwh || j.position[2]<cwh
                if loc_1!=loc_2
                    if !loc_2 && (self.warning || rand()<=1-j.break_rules)
                        j.radius = radius_with_masks
                    else
                        j.radius = radius_without_masks
                    end
                end
            end
        end
    end

    export House

end
