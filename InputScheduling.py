from SchedulingClass import *


def start_scheduling(gui, scheduling, processes, processors, pcore_idx, arrival_time_lst, burst_time_lst,
                     time_quantum=0):
    process_lst = []
    processor_lst = []
    queue_lst = []

    if scheduling == "FCFS":
        process_lst, processor_lst, queue_lst = FCFS(gui, processes, processors, pcore_idx, arrival_time_lst,
                                                     burst_time_lst) \
            .multi_processing()
    elif scheduling == "RR":
        process_lst, processor_lst, queue_lst = RR(gui, processes, processors, pcore_idx, arrival_time_lst,
                                                   burst_time_lst,
                                                   time_quantum) \
            .multi_processing()
    elif scheduling == "SPN":
        process_lst, processor_lst, queue_lst = SPN(gui, processes, processors, pcore_idx, arrival_time_lst,
                                                    burst_time_lst) \
            .multi_processing()
    elif scheduling == "SRTN":
        process_lst, processor_lst, queue_lst = SRTN(gui, processes, processors, pcore_idx, arrival_time_lst,
                                                     burst_time_lst) \
            .multi_processing()
    elif scheduling == "HRRN":
        process_lst, processor_lst, queue_lst = HRRN(gui, processes, processors, pcore_idx, arrival_time_lst,
                                                     burst_time_lst) \
            .multi_processing()
    else:
        process_lst, processor_lst, queue_lst = P_HRRN(gui, processes, processors, pcore_idx,
                                                                          arrival_time_lst, burst_time_lst, time_quantum) \
            .multi_processing()

    return process_lst, processor_lst, queue_lst
