from SchedulingClass import *

if __name__ == '__main__':
    # 스케줄링 종류입력
    scheduling = input("scheduling : ")
    scheduling = scheduling.upper()
    # 프로세스 개수 입력
    processes = int(input("Processes : "))
    # 프로세서 개수 입력
    processors = int(input("Processors : "))
    # pcore로 설정할 프로세서 번호 입력(없을시 입력없이 enter)
    pcore_idx = list(input("Pcore index : ").split(" "))
    # 프로세스 순서대로 도착시간 입력
    arrival_time_lst = list(map(int, input("Arrival Time : ").split(" ")))
    # 프로세스 순서대로 실행시간 입력
    burst_time_lst = list(map(int, input("Burst Time : ").split(" ")))
    # time-quantum 입력
    time_quantum = int(input("time-quantum : "))

    process_lst = []
    processor_lst = []
    queue_lst = []

    if scheduling == "FCFS":
        process_lst, processor_lst, queue_lst = FCFS(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst)\
            .multi_processing()
    elif scheduling == "RR":
        process_lst, processor_lst, queue_lst = RR(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst, time_quantum)\
            .multi_processing()
    elif scheduling == "SPN":
        process_lst, processor_lst, queue_lst = SPN(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst)\
            .multi_processing()
    elif scheduling == "SRTN":
        process_lst, processor_lst, queue_lst = SRTN(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst)\
            .multi_processing()
    elif scheduling == "HRRN":
        process_lst, processor_lst, queue_lst = HRRN(processes, processors, pcore_idx, arrival_time_lst, burst_time_lst)\
            .multi_processing()

    print(process_lst)          # 프로세스정보 출력
    print("-----------")
    print(processor_lst)        # 프로세서정보 출력
    print("-----------")
    print(queue_lst)            # 레디큐 정보 출력

