module human
    include("./fixed_parameters.jl")
    using .fixed_parameters

    mutable struct Human
        radius::Float64
        position::Tuple
        intern::Bool
        random_infection_rate::Float64
        infected::Bool
        infected_time::Int64
        show_infection_sign::Bool
        in_quarantine::Bool
        quarantine_time::Int64
        immunized::Bool
        alive::Bool
        destination::Any
        step::Float64
        break_rules::Float64

        contact::Any
        get_override_permission::Any
        move::Any

        function Human(spawnpoint::Tuple{Float64, Float64}, break_rules::Float64, intern::Bool, random_infection_rate::Float64)
            new(radius_without_masks, spawnpoint, intern, random_infection_rate, false, 0, false, false, 0, false, true, nothing, move_speed, break_rules, contact, get_override_permission, move)
        end
    end

    function contact(self::Human, human::Any)
        distance = sqrt((self.position[1]-human.position[1])^2+(self.position[2]-human.position[2])^2)
        if distance>=radius_without_masks
            return false
        end
        infection_distance = get_infection_distance(self.radius, human.radius)
        if distance < infection_distance
            infection_rate = get_infection_rate(distance, infection_distance)
            infection_active_rate = get_infection_active_rate(self.infected_time/day_tick)
            if rand()<=infection_rate*infection_active_rate
                human.infected = true
                return true
            end
        end
        return false
    end

    function get_override_permission(self::Human, fakewalls::Array)
        for wall in lundwalls
            if !(wall in fakewalls) && wall[1][1]>min(self.position[1], self.destination[1]) && wall[1][1]<max(self.position[1], self.destination[1])
                height = ((self.destination[2]-self.position[2])/(self.destination[1]-self.position[1]))*(wall[1][1]-self.position[1])+self.position[2]
                if height>=wall[2][1] && height<=wall[2][2]
                    return true
                end
            end
        end
        return false
    end

    function move(self::Human, fakewalls::Array)
        if !self.alive || self.in_quarantine
            return nothing
        end
        if self.destination==nothing || rand()<=move_random_rate
            angle = rand(1:360)
            x = cos(angle)*self.step
            y = sin(angle)*self.step
        else
            destination_override = self.get_override_permission(self, fakewalls)
            if destination_override
                temp = self.destination
                if self.position[2]<=cwh || self.position[2]>=lund_size[2]-hwh
                    self.destination = (self.position[1], rand(cwh:0.01:lund_size[2]-hwh))
                else
                    self.destination = (self.destination[1], rand(cwh:0.01:lund_size[2]-hwh))
                end
            end
            length_x = self.destination[1]-self.position[1]
            length_y = self.destination[2]-self.position[2]
            x = (self.step*length_x)/sqrt(length_x^2+length_y^2)
            y = (self.step*length_y)/sqrt(length_x^2+length_y^2)
            if destination_override
                self.destination = temp
            end
        end
        new_position = [self.position[1]+x, self.position[2]+y]

        for wall in lundwalls
            if !(wall in fakewalls) && wall[1][1]<max(new_position[1], self.position[1]) && wall[1][1]>min(new_position[1], self.position[1])
                height = (y*(wall[1][1]-self.position[1]))/x+self.position[2]
                if height>=wall[2][1] && height<=wall[2][2]
                    new_position[1] = wall[1][1]-(x/abs(x))*d
                end
                break
            end
        end
        for i in 1:2
            if new_position[i] < d
                new_position[i] = d
            elseif new_position[i] > lund_size[i]-d
                new_position[i] = lund_size[i]-d
            end
        end
        for wall in lundwalls
            if !(wall in fakewalls) && abs(new_position[1]-wall[1][1]) < d
                new_position[1] = wall[1][1]+((new_position[1]-wall[1][1])*d)/abs(new_position[1]-wall[1][1])
            end
        end
        self.position = Tuple(new_position)
    end

    export Human

end
