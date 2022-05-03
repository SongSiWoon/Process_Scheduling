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

    def peek(self):
        if not self.isEmpty(): return self.items[0]

    # queue 사이즈
    def size(self):
        return len(self.items)

    # 프로세스 도착시 레디큐에 추가
    def inready(self, process_lst, time):
        for process in process_lst:
            if process.at == time:
                self.enqueue(process)

    def __str__(self):
        return "[" + (" ".join(str(s.id) for s in self.items)) + "]"


# SPN전용 readyQueue
class SPNReadyQueue(ReadyQueue):
    def __init__(self):
        super(SPNReadyQueue, self).__init__()

    def enqueue(self, item):
        self.items.append(item)
        self.items.sort(key=lambda process: process.bt)

    # # 실행시간이 적은 프로세스에게 우선순위르 부여하는 dequeue 재정의
    # def dequeue(self):
    #     if not self.isEmpty():
    #         priority = 0
    #         for i in range(1, self.size()):
    #             if self.items[i].bt < self.items[priority].bt:
    #                 priority = i
    #         return self.items.pop(priority)


# SRTN전용 readyQueue
class SRTNReadyQueue(ReadyQueue):
    def __init__(self):
        super(SRTNReadyQueue, self).__init__()

    def enqueue(self, item):
        self.items.append(item)
        self.items.sort(key=lambda process: process.cbt)

    # # 잔여 실행시간이 적은 프로세스에게 우선순위를 부여하는 dequeue 재정의
    # def dequeue(self):
    #     if not self.isEmpty():
    #         priority = 0
    #         for i in range(1, self.size()):
    #             if self.items[i].cbt < self.items[priority].cbt:
    #                 priority = i
    #         return self.items.pop(priority)
    #
    # # 현재 running 상태는 프로세스 잔여시간과 ready 프로세스의 잔여시간 비교를 위한 peek 재정의
    # def peek(self):
    #     if not self.isEmpty():
    #         priority = 0
    #         for i in range(1, self.size()):
    #             if self.items[i].cbt < self.items[priority].cbt:
    #                 priority = i
    #         return self.items[priority]


# HRRN전용 readyQueue
class HRRNReadyQueue(ReadyQueue):
    def __init__(self):
        super(HRRNReadyQueue, self).__init__()

    def enqueue(self, item):
        self.items.append(item)
        self.items.sort(key=lambda process: process.get_response_ratio(), reverse=True)

    # def dequeue(self):
    #     priority = self.items.index(max(self.items, key=lambda process: process.get_response_ratio()))
    #     return self.items.pop(priority)


class Process:

    def __init__(self, id, at, bt, tq=0):
        self.id = int(id)  # 프로세스 아이디
        self.bt = int(bt)  # 실행시간
        self.cbt = int(bt)  # 계산용 실행시간
        self.at = int(at)  # 도칙 시간
        self.wt = 0  # 대기 시간
        self.tt = 0  # 반환 시간
        self.ntt = 0  # 실행 시간 대비 대기 시간
        self.tq = int(tq)  # Time quantum for RR
        self.ctq = int(tq)  # 계산용 TQ

    # 프로세스 정보 업데이트
    def update_processinfo(self, time):
        self.tt = time - self.at
        self.ntt = round(self.tt / self.bt, 2)
        self.wt = self.tt - self.bt

    # HRRN을 위한 Response ratio 계산
    def get_response_ratio(self):
        return (self.wt + self.bt) / self.bt

    # 프로세스 정보 출력
    def __str__(self):
        return "Process" + str(self.id) + " AT = " + str(self.at) + " BT = " + str(self.bt) + " TT = " + str(
            self.tt) + " NTT = " + str(self.ntt) + " WT = " + str(self.wt)


class Processor:

    def __init__(self, id, core="e"):
        self.id = int(id)  # 프로세서 아이디
        self.process = None  # 할당된 프로세스
        self.core = core  # 프로세서 코어 종류
        self.running = False  # 프로세서 상태
        self.power_consum = 0  # 소비 전력
        self.power_waiting = 0  # 대기 전력
        self.memory = []  # 프로세스 기록

    # 프로세스 할당
    def dispatch(self, readyQueue: ReadyQueue):
        if not readyQueue.isEmpty():
            if not self.running:
                self.process = readyQueue.dequeue()
                self.running = True

    # Ecore 프로세스 실행 -> 프로세스 cbt를 1 감소, 소비전력 1증가, 대기전력 0.1증가
    def Ecore_running(self, time, gui):
        if self.process is not None:
            self.memory.append(self.process.id)
            gui.setGTable(self.process.id, time)
            if self.running:
                self.process.cbt -= 1
                self.power_consum += 1  # Ecore의 소비전력 계산
                if self.process.cbt == 0:
                    self.running = False
                    self.process.update_processinfo(time)  # 프로스세가 종료되면 tt, ntt, wt 업데이트
                    self.process = None
                    return 1
        else:
            self.memory.append(None)
            self.power_waiting += 0.1  # Ecore의 대기전력 계산
        return 0

    # Pcore 프로세스 실행 -> 프로세스 cbr를 2감소, 소비 전력 3증가, 대기전력 0.1증가
    def Pcore_running(self, time, gui):
        if self.process is not None:
            self.memory.append(self.process.id)
            gui.setGTable(self.process.id, time)
            if self.running:
                self.process.cbt -= 2  # Ecore대비 2배의 성능
                self.power_consum += 3  # Ecore대비 소비전력 3배 계산
                if self.process.cbt <= 0:
                    self.running = False
                    self.process.update_processinfo(time)  # 프로스세가 종료되면 tt, ntt, wt 업데이트
                    self.process = None
                    return 1
        else:
            self.memory.append(None)
            self.power_waiting += 0.1
        return 0

    # time-quantum 확인
    def check_time_quantum(self, readyQueue: ReadyQueue):
        if self.running:
            self.process.ctq -= 1  # 현재 실행중인 프로세스 time-quantum 감소
            if self.process.ctq == 0:  # time-quantum이 0일때 다름 프로세스한테 선점당함
                self.running = False
                readyQueue.enqueue(self.process)
                self.process.ctq = self.process.tq  # 다시 ctq time-quantum을 초기화
                self.process = None


class Scheduling:
    def __init__(self, gui, process_n, processor_n, p_core_lst, at_lst, bt_lst, tq=0):
        self.gui = gui
        self.process_lst = []  # 입력된 프로세스 리스트
        self.processor_lst = []  # 입력된 프로세서 리스트
        self.readyQueue = None  # readyQueue
        self.queue_memory = []  # redyQueue에 저장되는 프로세스 기록하기위한 리스트
        self.process_n = int(process_n)  # 프로세스의 수
        self.processor_n = int(processor_n)  # 프로세서의 수
        self.pcore_index = p_core_lst  # Pcore인 프로세서 id 리스트
        self.bt_lst = bt_lst  # 입력받은 실행시간 리스트
        self.at_lst = at_lst  # 입력받은 도착시간 리스트
        self.tq = tq  # 입력받은 time-quantum

        self.init_process()
        self.init_processor()

    # 입력받은 정보들로 프로세스 객체 생성
    def init_process(self):
        for i in range(self.process_n):
            self.process_lst.append(Process(i + 1, self.at_lst[i], self.bt_lst[i], self.tq))

    # 입력받은 정보들로 프로세서 객체 생성
    def init_processor(self):
        for i in range(self.processor_n):
            if str(i + 1) in self.pcore_index:
                self.processor_lst.append(Processor(i + 1, "p"))
            else:
                self.processor_lst.append(Processor(i + 1))

    # 프로세스 멀티 프로세싱으로 실행
    def multi_processing(self):
        time = 0  # 전체시간
        termination = 0  # 종료된 프로세스의 수

        # 종료된 프로세스의 수와 입력된 프로세스의 수가 같을때 까지 실행
        while termination != self.process_n:
            self.readyQueue.inready(self.process_lst, time)  # 새롭게 들어오는 프로세스 readyqueue에 추가
            self.queue_memory.append(self.output_ReadyQueue_info(self.readyQueue))  # 현재 레디큐에 있는 프로세스를 반환하기위해 저장
            time += 1
            for processor in self.processor_lst:
                processor.dispatch(self.readyQueue)  # 현재 비어있는 프로세서에 프로세스 할당
                if processor.core == "e":
                    termination += processor.Ecore_running(time)
                else:
                    termination += processor.Pcore_running(time)

        process_info = self.output_process_info()  # 프로세스 정보들 반환
        processor_info = self.output_processor_info()  # 프로세서 정보들 반환
        queue_info = self.queue_memory  # 레디큐 히스토리 반환
        return process_info, processor_info, queue_info

    # 프로세스의 id, at, bt, wt, tt, ntt 반환
    def output_process_info(self):
        process_info = []
        for process in self.process_lst:
            process_info.append((process.id, process.at, process.bt, process.wt, process.tt, process.ntt))

        return process_info

    # 프로세서의 id, core종류, 소비 전력, 할당됬던 프로세스id 반환
    def output_processor_info(self):
        processor_info = []

        for processor in self.processor_lst:
            power = processor.power_consum + processor.power_waiting
            processor_info.append((processor.id, processor.core, power, processor.memory))

        return processor_info

    # readyqueue에 들어왔던 프로세스 id 반환
    def output_ReadyQueue_info(self, readyQueue):
        res = []
        for process in readyQueue.items:
            res.append(process.id)
        return res


class FCFS(Scheduling):

    def __init__(self, process_n, processor_n, p_core_lst, at_lst, bt_lst):
        super(FCFS, self).__init__(process_n, processor_n, p_core_lst, at_lst, bt_lst)
        self.readyQueue = ReadyQueue()


class RR(Scheduling):

    def __init__(self, process_n, processor_n, p_core_lst, at_lst, bt_lst, tq):
        super(RR, self).__init__(process_n, processor_n, p_core_lst, at_lst, bt_lst, tq)
        self.readyQueue = ReadyQueue()

    def multi_processing(self):
        time = 0
        termination = 0

        while termination != self.process_n:
            self.readyQueue.inready(self.process_lst, time)
            self.queue_memory.append(self.output_ReadyQueue_info(self.readyQueue))
            time += 1
            for processor in self.processor_lst:
                processor.check_time_quantum(self.readyQueue)  # RR은 time-quantum확인하는 로직 추가
                processor.dispatch(self.readyQueue)
                if processor.core == "e":
                    termination += processor.Ecore_running(time)
                else:
                    termination += processor.Pcore_running(time)

        process_info = self.output_process_info()
        processor_info = self.output_processor_info()
        queue_info = self.queue_memory
        return process_info, processor_info, queue_info


class SPN(Scheduling):
    def __init__(self, process_n, processor_n, p_core_lst, at_lst, bt_lst):
        super(SPN, self).__init__(process_n, processor_n, p_core_lst, at_lst, bt_lst)
        self.readyQueue = SPNReadyQueue()  # SRN전용 Queue사용


class SRTN(Scheduling):
    def __init__(self, process_n, processor_n, p_core_lst, at_lst, bt_lst):
        super(SRTN, self).__init__(process_n, processor_n, p_core_lst, at_lst, bt_lst)
        self.readyQueue = SRTNReadyQueue()  # SRTN전용 Queue사용

    def multi_processing(self):
        time = 0
        termination = 0

        while termination != self.process_n:
            self.readyQueue.inready(self.process_lst, time)
            self.queue_memory.append(self.output_ReadyQueue_info(self.readyQueue))
            time += 1
            for processor in self.processor_lst:
                processor.dispatch(self.readyQueue)
                if processor.core == "e":
                    termination += processor.Ecore_running(time)
                else:
                    termination += processor.Pcore_running(time)

                if processor.running and processor.process is not None and not self.readyQueue.isEmpty():
                    # 현재 실행중인 프로세스의 남은 실행시간과 readyQueue에서 남은 실행시간이 가장 적은 값과 비교
                    if processor.process.cbt > self.readyQueue.peek().cbt:
                        processor.running = False
                        self.readyQueue.enqueue(processor.process)
                        processor.process = None

        process_info = self.output_process_info()
        processor_info = self.output_processor_info()
        queue_info = self.queue_memory
        return process_info, processor_info, queue_info


class HRRN(Scheduling):
    def __init__(self, process_n, processor_n, p_core_lst, at_lst, bt_lst):
        super(HRRN, self).__init__(process_n, processor_n, p_core_lst, at_lst, bt_lst)
        self.readyQueue = HRRNReadyQueue()  # HRRN전용 Queue 사용

    def multi_processing(self):
        time = 0
        termination = 0

        while termination != self.process_n:
            self.readyQueue.inready(self.process_lst, time)
            self.queue_memory.append(self.output_ReadyQueue_info(self.readyQueue))
            time += 1
            for processor in self.processor_lst:
                processor.dispatch(self.readyQueue)
                if processor.core == "e":
                    termination += processor.Ecore_running(time)
                else:
                    termination += processor.Pcore_running(time)
            # response_ratio계산을 위해 readyQueue에 있는 프로세스들의 wt 업데이트
            for process in self.readyQueue.items:
                process.wt += 1

        process_info = self.output_process_info()
        processor_info = self.output_processor_info()
        queue_info = self.queue_memory
        return process_info, processor_info, queue_info
