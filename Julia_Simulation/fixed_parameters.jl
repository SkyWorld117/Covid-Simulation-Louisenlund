module fixed_parameters
    tick_second_rate = 1
    coord_meter_rate = 1

    # Basic
    window_size = (16, 7)

    radius_with_masks = 0.4*coord_meter_rate
    radius_without_masks = 1.5*coord_meter_rate

    move_random_rate = 0.2
    move_speed = (coord_meter_rate*1.5)/tick_second_rate
    indoor_speed = (coord_meter_rate*0.5)/tick_second_rate
    quarantine_speed = (coord_meter_rate*0.2)/tick_second_rate

    day_tick = 86400*tick_second_rate÷60
    sim_time = 10

    end_infection_time = 14
    death_rate = 0.40
    fake_negative_test = 0.04

    # Advanced
    infection_period = 60÷60
    d = radius_without_masks/2

    lund_size = (400, 90)
    cwh, hwh = 10, 10
    lundbounds = [([0,lund_size[1]], [lund_size[2],lund_size[2]]), ([0,lund_size[1]], [0,0]), ([0,0], [0,lund_size[2]]), ([lund_size[1],lund_size[1]], [0,lund_size[2]])]

    num_in = [16,16,20,12,21,14,2,3,23,7,6,7,11,16,12,13,6,14,11,17,7,14,21,4,4,4]
    num_intern_students = 301
    num_houses = length(num_in)
    num_classrooms = 30
    lundwalls = Array{Tuple}(undef, num_houses+num_classrooms-2)
    start = 0.0
    for i in 1:num_houses-1
        global start
        start += num_in[i]/num_intern_students*lund_size[1]
        lundwalls[i] = ([start,start], [lund_size[2]-hwh,lund_size[2]])
    end
    start = 0.0
    for i in num_houses:num_houses+num_classrooms-2
        global start
        start += 1/num_classrooms*lund_size[1]
        lundwalls[i] = ([start,start], [0,cwh])
    end

    function get_infection_distance(radius_1::Float64, radius_2::Float64)
        return max(radius_1, radius_2)-abs((radius_1-radius_2)/2)
    end

    function get_infection_rate(distance::Float64, infection_distance::Float64)
        return (0.95/infection_distance)*((infection_distance-distance)/(distance+1))
    end

    function get_show_infection_sign_rate(days)
        return 0.00156566*days^3-0.0493434*days^2+0.383939*days
    end

    function get_infection_active_rate(days)
        return exp((days-5.7)/1.1)/(exp((days-5.7)/1.1)+1)
    end

    function get_cure_rate(days)
        return log(end_infection_time-days+1)/log(end_infection_time+1)
    end

    export tick_second_rate, coord_meter_rate, window_size, radius_with_masks, radius_without_masks, move_random_rate, move_speed, indoor_speed, quarantine_speed, day_tick, sim_time, end_infection_time, death_rate, fake_negative_test, infection_period, d, lund_size, lundbounds, lundwalls, hwh, cwh, num_houses, num_classrooms, get_infection_distance, get_infection_rate, get_infection_active_rate, get_show_infection_sign_rate, get_cure_rate
end
