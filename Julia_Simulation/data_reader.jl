using HDF5
using Plots

mode = 2
folder_dir = "./Data/default_c=4_5/"

if mode==1
    for i in 0.0:0.2:1.0
        path = folder_dir*"break_rules="*string(i)*".h5"
        h5open(path, "r") do file
            data = read(file, "data")
            #plot(data[1,:], [data[2,:], data[3,:], data[4,:], data[5,:], data[6,:]])
            plot(data[1,:], data[2,:])
            savefig(folder_dir*"break_rules="*string(i)*".svg")
        end
    end
end

if mode==2
    path = folder_dir
    data = Any[[], [], [], [], [], []]
    for i in 0.0:0.2:1.0
        h5open(path*"break_rules="*string(i)*".h5", "r") do file
            global data
            data[Int(i*5+1)] = read(file, "data")
        end
    end
    plot(data[1][1,:], data[1][2,:])
    for i in 2:6
        plot!(data[i][1,:], data[i][2,:])
    end
    savefig(path*"summary.svg")
end
