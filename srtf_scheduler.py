import heapq

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None

    def __lt__(self, other):
        return self.remaining_time < other.remaining_time

def srtf_scheduler(processes):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    n = len(processes)
    current_time = 0
    completed = 0
    ready_queue = []
    time_chart = []
    log = []
    
    log.append(f"{n} processes")
    log.append("Using preemptive Shortest Job First")

    while completed != n:
        for process in processes:
            if process.arrival_time == current_time:
                log.append(f"Time {current_time:3} : P{process.pid:02} arrived")
                heapq.heappush(ready_queue, process)

        if ready_queue:
            current_process = heapq.heappop(ready_queue)
            
            if current_process.start_time is None:
                current_process.start_time = current_time

            if not time_chart or time_chart[-1] != current_process.pid:
                log.append(f"Time {current_time:3} : P{current_process.pid:02} selected (burst {current_process.remaining_time:3})")

            time_chart.append(current_process.pid)
            current_process.remaining_time -= 1
            current_time += 1
            
            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                log.append(f"Time {current_time:3} : P{current_process.pid:02} finished")
                completed += 1
            else:
                heapq.heappush(ready_queue, current_process)
        else:
            time_chart.append("Idle")
            current_time += 1

    log.append(f"Time {current_time:3} : Idle")
    log.append(f"Finished at time {current_time:3}")

    return processes, time_chart, log

def calculate_wait_turnaround_times(processes):
    result = []
    for process in processes:
        wait_time = process.completion_time - process.arrival_time - process.burst_time
        turnaround_time = process.completion_time - process.arrival_time
        response_time = process.start_time - process.arrival_time
        result.append((process.pid, wait_time, turnaround_time, response_time))
    return result