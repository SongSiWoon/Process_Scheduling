from enum import Enum


class ProcessSate(Enum):
    Ready = 0
    Running = 1
    Termination = 3


class ReadyQueue:
    # 생성자
    def __init__(self):
        self.items = []

    # 레디큐가 비었는지 확인
    def isEmpty(self):
        return len(self.items) == 0

    # 레디큐에 아이템 추가
    def enqueue(self, item):
        self.items.append(item)

    # 레디큐 앞에서부터 아이템 꺼내기
    def dequeue(self):
        if not self.isEmpty(): return self.items.pop(0)

    # queue 사이즈
    def size(self):
        return len(self.items)

    # 프로세스 도착시 레디큐에 추가
    def inReady(self, process_lst, time):
        for process in process_lst:
            if process.at == time:
                self.enqueue(process)

    def __str__(self):
        return "[" + (" ".join(str(s.id) for s in self.items)) + "]"

class Process:

    def __init__(self, id, at, bt, tq=0):
        self.id = int(id)   # 프로세스 아이디
        self.bt = int(bt)   # 실행시간
        self.cbt = int(bt)  # 계산용 실행시간
        self.at = int(at)   # 도칙 시간
        self.wt = 0         # 대기 시간
        self.tt = 0         # 반환 시간
        self.ntt = 0        # 실행 시간 대비 대기 시간
        self.tq = int(tq)   # Time quantum for RR
        self.ctq = int(tq)  # 계산용 TQ

    # 프로세스 정보 업데이트
    def update_processinfo(self, time):
        self.tt = time - self.at
        self.ntt = round(self.tt / self.bt, 2)
        self.wt = self.tt - self.bt

    # 프로세스 정보 출력
    def __str__(self):
        return "Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.bt) + " TT = " + str(
            self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)


class Processor:

    def __init__(self, id, core="e"):
        self.id = int(id)       # 프로세서 아이디
        self.process = None     # 할당된 프로세스
        self.core = core        # 프로세서 코어 종류
        self.running = False    # 프로세서 상태
        self.power_consum = 0   # 소비 전력
        self.power_waiting = 0  # 대기 전력
        self.memory = []        # 프로세스 기록

    # 프로세스 할당
    def dispatch(self, readyQueue: ReadyQueue):
        if not readyQueue.isEmpty():
            if not self.running:
                self.process = readyQueue.dequeue()
                self.running = True

    # Ecore 프로세스 실행 -> 프로세스 cbt를 1 감소, 소비전력 1증가, 대기전력 0.1증가
    def Ecore_running(self, time):
        if self.process is not None:
            self.memory.append(self.process.id)
            if self.running:
                self.process.cbt -= 1
                self.power_consum += 1
                if self.process.cbt == 0:
                    self.running = False
                    self.process.update_processinfo(time)
                    self.process = None
                    return 1
        else:
            self.memory.append(None)
            self.power_waiting += 0.1
        return 0

    # Pcore 프로세스 실행 -> 프로세스 cbr를 2감소, 소비 전력 3증가, 대기전력 0.1증가
    def Pcore_running(self, time):
        if self.process is not None:
            self.memory.append(self.process.id)
            if self.running:
                self.process.cbt -= 2
                self.power_consum += 3
                if self.process.cbt <= 0:
                    self.running = False
                    self.process.update_processinfo(time)
                    self.process = None
                    return 1
        else:
            self.memory.append(None)
            self.power_waiting += 0.1
        return 0

    def check_time_quantum(self, readyQueue:ReadyQueue):
        if self.running:
            self.process.ctq -= 1
            if self.process.ctq == 0:
                self.running = False
                readyQueue.enqueue(self.process)
                self.process.ctq = self.process.tq
                self.process = None


class FCFS:

    def __init__(self, process_n, processor_n, p_core_lst, at_lst, bt_lst):
        self.process_lst = []
        self.processor_lst = []
        self.pcore_index = p_core_lst
        self.readyQueue = ReadyQueue()

        self.process_n = int(process_n)
        self.processor_n = int(processor_n)
        self.bt_lst = bt_lst
        self.at_lst = at_lst

        for i in range(self.process_n):
            self.process_lst.append(Process(i + 1, at_lst[i], bt_lst[i]))

        for i in range(self.processor_n):
            if str(i + 1) in p_core_lst:
                self.processor_lst.append(Processor(i + 1, "p"))
            else:
                self.processor_lst.append(Processor(i + 1))

    def multi_processing(self):
        time = 0
        exit = 0

        while exit != self.process_n:
            self.readyQueue.inReady(self.process_lst, time)
            time += 1
            for processor in self.processor_lst:
                processor.dispatch(self.readyQueue)
                if processor.core == "e":
                    exit += processor.Ecore_running(time)
                else:
                    exit += processor.Pcore_running(time)


        process_m = []
        for process in self.process_lst:
            process_m.append((process.id, process.at, process.bt, process.wt, process.tt, process.ntt))

        processor_m = []
        for processor in self.processor_lst:
            processor_m.append(processor.core)
            processor_m.append(processor.power_consum + processor.power_waiting)
            processor_m.append(processor.memory)

        return (process_m, processor_m)


class RR:
    def __init__(self, process_n, processor_n,p_core_lst, at_lst, bt_lst, tq):
        self.process_lst = []
        self.processor_lst = []
        self.pcore_index = p_core_lst
        self.readyQueue = ReadyQueue()
        self.process_n = int(process_n)
        self.processor_n = int(processor_n)
        self.bt_lst = bt_lst
        self.at_lst = at_lst

        for i in range(self.process_n):
            self.process_lst.append(Process(i + 1, at_lst[i], bt_lst[i], tq))

        for i in range(self.processor_n):
            if str(i + 1) in p_core_lst:
                self.processor_lst.append(Processor(i + 1, "p"))
            else:
                self.processor_lst.append(Processor(i + 1))

    def multi_processing(self):
        time = 0
        exit = 0

        while exit != self.process_n:
            self.readyQueue.inReady(self.process_lst, time)
            time += 1
            for processor in self.processor_lst:
                processor.check_time_quantum(self.readyQueue)
                processor.dispatch(self.readyQueue)
                if processor.core == "e":
                    exit += processor.Ecore_running(time)
                else:
                    exit += processor.Pcore_running(time)

        res = []
        for process in self.process_lst:
            res.append((process.id, process.at, process.bt, process.wt, process.tt, process.ntt))
        processor_m = []
        for processor in self.processor_lst:
            processor_m.append(processor.core)
            processor_m.append(processor.power_consum + processor.power_waiting)
            processor_m.append(processor.memory)

        return (res, processor_m)
