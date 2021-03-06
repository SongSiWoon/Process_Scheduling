import Test_SchedulingClass
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


def test_scheduling(scheduling, processes, processors, pcore_idx, arrival_time_lst, burst_time_lst, time_quantum=0):
    process_lst = []
    processor_lst = []
    queue_lst = []

    if scheduling == "FCFS":
        process_lst, processor_lst, queue_lst = Test_SchedulingClass.FCFS(processes, processors, pcore_idx,
                                                                          arrival_time_lst, burst_time_lst) \
            .multi_processing()
    elif scheduling == "RR":
        process_lst, processor_lst, queue_lst = Test_SchedulingClass.RR(processes, processors, pcore_idx,
                                                                        arrival_time_lst, burst_time_lst,
                                                                        time_quantum) \
            .multi_processing()
    elif scheduling == "SPN":
        process_lst, processor_lst, queue_lst = Test_SchedulingClass.SPN(processes, processors, pcore_idx,
                                                                         arrival_time_lst, burst_time_lst) \
            .multi_processing()
    elif scheduling == "SRTN":
        process_lst, processor_lst, queue_lst = Test_SchedulingClass.SRTN(processes, processors, pcore_idx,
                                                                          arrival_time_lst, burst_time_lst) \
            .multi_processing()
    elif scheduling == "HRRN":
        process_lst, processor_lst, queue_lst = Test_SchedulingClass.HRRN(processes, processors, pcore_idx,
                                                                          arrival_time_lst, burst_time_lst) \
            .multi_processing()
    else:
        process_lst, processor_lst, queue_lst = Test_SchedulingClass.P_HRRN(processes, processors, pcore_idx,
                                                                          arrival_time_lst, burst_time_lst, time_quantum) \
            .multi_processing()
    return process_lst, processor_lst, queue_lst


if __name__ == '__main__':
    # ???????????? ????????????
    scheduling = input("scheduling : ")
    scheduling = scheduling.upper()
    # ???????????? ?????? ??????
    processes = int(input("Processes : "))
    # ???????????? ?????? ??????
    processors = int(input("Processors : "))
    # pcore??? ????????? ???????????? ?????? ??????(????????? ???????????? enter)
    pcore_idx = list(input("Pcore index : ").split(" "))
    # ???????????? ???????????? ???????????? ??????
    arrival_time_lst = list(map(int, input("Arrival Time : ").split(" ")))
    # ???????????? ???????????? ???????????? ??????
    burst_time_lst = list(map(int, input("Burst Time : ").split(" ")))
    # time-quantum ??????
    time_quantum = int(input("time-quantum : "))

    process_lst = []
    processor_lst = []
    queue_lst = []

    process_lst, processor_lst, queue_lst = \
        test_scheduling(scheduling, processes, processors, pcore_idx, arrival_time_lst, burst_time_lst, time_quantum)

    print(process_lst)  # ?????????????????? ??????
    print("-----------")
    print(processor_lst)  # ?????????????????? ??????
    print("-----------")
    print(queue_lst)  # ????????? ?????? ??????
