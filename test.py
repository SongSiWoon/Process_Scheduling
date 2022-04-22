from SchedulingClass import *


if __name__ == '__main__':
    processes = int(input("Processes : "))
    processors = int(input("Processors : "))
    pcore_idx = list(input("Pcore index : ").split(" "))
    arrival_time_lst = list(map(int, input("Arrival Time : ").split(" ")))
    burst_time_lst = list(map(int, input("Burst Time : ").split(" ")))

    #time_lst, p_lst = FCFS(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst).multi_processing()
    time_lst, p_lst = RR(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst, 2).multi_processing()

    print(time_lst)
    print("-----------")
    print(p_lst)
