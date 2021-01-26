module class
    include("./fixed_parameters.jl")
    using .fixed_parameters

    mutable struct Class
        warning::Bool
        num_students::Int64
        num_teachers::Int64

        pick::Any
        in_class::Any
        lessoning::Any

        crew::Array
        class_border::Tuple

        function Class(num_students::Int64, num_teachers::Int64)
            new(false, num_students, num_teachers, pick, in_class, lessoning)
        end
    end

    function pick(self::Class, crew::Array, start::Array)
        my_crew = [Array{Any}(undef, self.num_students), Array{Any}(undef, self.num_teachers)]
        for i in 1:2
            for j in 1:length(my_crew[i])
                my_crew[i][j] = crew[i][j+start[i]]
            end
        end
        self.crew = my_crew
    end

    function in_class(self::Class, position::Tuple)
        if position[1]>=self.class_border[1][1] && position[1]<=self.class_border[2][1] && position[2]>=self.class_border[2][2] && position[2]<=self.class_border[1][2]
            return true
        else
            return false
        end
    end

    function lessoning(self::Class, walls::Array, fakewalls::Array)
        self.class_border = ((walls[1][1][1],walls[1][2][2]), (walls[2][1][1],walls[2][2][1]))
        for i in self.crew
            for j in i
                if j.position==(nothing,nothing)
                    j.position = (rand(d:0.01:lund_size[1]-d), rand(cwh:0.01:lund_size[2]-hwh))
                end
                if !self.in_class(self, j.position) && (j.destination==nothing || !self.in_class(self, j.destination))
                    #println(self.class_border[2][1], " ", self.class_border[1][1])
                    j.destination = (rand(self.class_border[1][1]+d:0.01:self.class_border[2][1]-d), rand(self.class_border[2][2]+d:0.01:self.class_border[1][2]-d))
                    j.step = move_speed
                elseif self.in_class(self, j.position) && j.destination!=nothing && sqrt((j.destination[1]-j.position[1])^2+(j.destination[2]-j.position[2])^2)<j.step
                    j.destination = nothing
                    j.step = indoor_speed
                elseif self.in_class(self, j.position) && j.destination==nothing
                    j.step = indoor_speed
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

    export Class

end
