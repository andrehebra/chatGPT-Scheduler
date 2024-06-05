import heapq
import argparse
from collections import deque

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.start_time = -1
        self.end_time = -1

def parse_input(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    process_count = int(lines[0].split()[1])
    run_for = int(lines[1].split()[1])
    scheduling_type = lines[2].split()[1]
    quantum = int(lines[3].split()[1]) if scheduling_type == 'rr' else None
    processes = []
    
    start_index = 4 if scheduling_type == 'rr' else 3
    for i in range(start_index, start_index + process_count):
        parts = lines[i].split()
        name = parts[2]
        arrival = int(parts[4])
        burst = int(parts[6])
        processes.append(Process(name, arrival, burst))
    
    return process_count, run_for, scheduling_type, quantum, processes

def fifo_scheduler(processes, run_for):
    processes.sort(key=lambda p: p.arrival)
    timeline = []
    current_time = 0
    wait_times = {p.name: 0 for p in processes}
    response_times = {p.name: 0 for p in processes}
    turnaround_times = {p.name: 0 for p in processes}
    queue = deque()
    
    for time in range(run_for):
        for process in processes:
            if process.arrival == time:
                queue.append(process)
                timeline.append(f"Time {time}: {process.name} arrived")
        
        if queue:
            current_process = queue[0]
            if current_process.start_time == -1:
                current_process.start_time = time
                response_times[current_process.name] = time - current_process.arrival
                timeline.append(f"Time {time}: {current_process.name} selected (burst {current_process.burst})")
            current_process.remaining -= 1
            if current_process.remaining == 0:
                current_process.end_time = time + 1
                turnaround_times[current_process.name] = current_process.end_time - current_process.arrival
                wait_times[current_process.name] = current_process.end_time - current_process.arrival - current_process.burst
                timeline.append(f"Time {time + 1}: {current_process.name} finished")
                queue.popleft()
        else:
            timeline.append(f"Time {time}: Idle")
    
    return timeline, wait_times, response_times, turnaround_times

def sjf_scheduler(processes, run_for):
    processes.sort(key=lambda p: p.arrival)
    timeline = []
    current_time = 0
    wait_times = {p.name: 0 for p in processes}
    response_times = {p.name: 0 for p in processes}
    turnaround_times = {p.name: 0 for p in processes}
    heap = []
    arrived = []
    finished = []
    
    for time in range(run_for):
        for process in processes:
            if process.arrival == time:
                heapq.heappush(arrived, (process.burst, process))
                timeline.append(f"Time {time}: {process.name} arrived")
        
        if heap:
            current_process = heapq.heappop(heap)[1]
            if current_process.start_time == -1:
                current_process.start_time = time
                response_times[current_process.name] = time - current_process.arrival
                timeline.append(f"Time {time}: {current_process.name} selected (burst {current_process.remaining})")
            current_process.remaining -= 1
            if current_process.remaining == 0:
                current_process.end_time = time + 1
                turnaround_times[current_process.name] = current_process.end_time - current_process.arrival
                wait_times[current_process.name] = current_process.end_time - current_process.arrival - current_process.burst
                timeline.append(f"Time {time + 1}: {current_process.name} finished")
                finished.append(current_process)
            else:
                heapq.heappush(heap, (current_process.remaining, current_process))
        else:
            timeline.append(f"Time {time}: Idle")
    
    return timeline, wait_times, response_times, turnaround_times

def round_robin_scheduler(processes, run_for, quantum):
    processes.sort(key=lambda p: p.arrival)
    timeline = []
    current_time = 0
    wait_times = {p.name: 0 for p in processes}
    response_times = {p.name: 0 for p in processes}
    turnaround_times = {p.name: 0 for p in processes}
    queue = deque()
    arrived = []
    for process in processes:
        arrived.append(process)
    
    current_process = None
    remaining_quantum = 0

    for time in range(run_for):
        # Add new arrivals to the queue
        for process in arrived:
            if process.arrival == time:
                queue.append(process)
                timeline.append(f"Time {time}: {process.name} arrived")
        
        if current_process is None or remaining_quantum == 0:
            if current_process is not None and current_process.remaining > 0:
                queue.append(current_process)
            if queue:
                current_process = queue.popleft()
                if current_process.start_time == -1:
                    current_process.start_time = time
                    response_times[current_process.name] = time - current_process.arrival
                timeline.append(f"Time {time}: {current_process.name} selected (burst {current_process.remaining})")
                remaining_quantum = quantum
        
        if current_process is not None:
            current_process.remaining -= 1
            remaining_quantum -= 1
            if current_process.remaining == 0:
                current_process.end_time = time + 1
                turnaround_times[current_process.name] = current_process.end_time - current_process.arrival
                wait_times[current_process.name] = current_process.end_time - current_process.arrival - current_process.burst
                timeline.append(f"Time {time + 1}: {current_process.name} finished")
                current_process = None
        
        if not current_process and not queue:
            timeline.append(f"Time {time}: Idle")
    
    return timeline, wait_times, response_times, turnaround_times

def print_report(process_count, scheduling_type, timeline, wait_times, response_times, turnaround_times, run_for):
    print(f"{process_count} processes")
    print(f"Using {scheduling_type}")
    for event in timeline:
        print(event)
    for time in range(run_for, run_for + (run_for - len(timeline))):
        print(f"Time {time}: Idle")
    print(f"Finished at time {run_for}")
    
    for name in wait_times:
        print(f"{name} wait {wait_times[name]} turnaround {turnaround_times[name]} response {response_times[name]}")

def main(file):
    process_count, run_for, scheduling_type, quantum, processes = parse_input(file)
    if scheduling_type == 'fifo':
        timeline, wait_times, response_times, turnaround_times = fifo_scheduler(processes, run_for)
    elif scheduling_type == 'sjf':
        timeline, wait_times, response_times, turnaround_times = sjf_scheduler(processes, run_for)
    elif scheduling_type == 'rr':
        timeline, wait_times, response_times, turnaround_times = round_robin_scheduler(processes, run_for, quantum)
    else:
        raise ValueError("Unknown scheduling type")
    
    print_report(process_count, scheduling_type, timeline, wait_times, response_times, turnaround_times, run_for)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a CPU scheduler.")
    parser.add_argument("filename", help="The input file containing process information.")
    args = parser.parse_args()
    
    main(args.filename)
