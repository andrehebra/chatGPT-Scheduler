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

def fcfs_scheduler(processes, run_for):
    timeline = []
    wait_times = {p.name: 0 for p in processes}
    response_times = {p.name: -1 for p in processes}
    turnaround_times = {p.name: 0 for p in processes}
    time = 0

    queue = deque()
    processes.sort(key=lambda p: p.arrival)
    process_index = 0
    current_process = None
    
    while time < run_for:
        # Add newly arrived processes to the queue
        while process_index < len(processes) and processes[process_index].arrival == time:
            process = processes[process_index]
            queue.append(process)
            timeline.append(f"Time {time:>4} : {process.name} arrived")
            process_index += 1
        
        if current_process:
            current_process.remaining -= 1
            if current_process.remaining == 0:
                current_process.end_time = time
                timeline.append(f"Time {time:>4} : {current_process.name} finished")
                turnaround_times[current_process.name] = time - current_process.arrival
                current_process = None
    
        # Select the next process from the queue if no current process
        if not current_process and queue:
            current_process = queue.popleft()
            # If the process is starting for the first time, log the start time
            if current_process.start_time == -1:
                current_process.start_time = time
                response_times[current_process.name] = time - current_process.arrival
            timeline.append(f"Time {time:>4} : {current_process.name} selected (burst {current_process.remaining:>3})")

        # Log idle time if no process is being executed and the queue is empty
        if not current_process and not queue:
            timeline.append(f"Time {time:>4} : Idle")
        
        time += 1

    # Calculate wait times
    for process in processes:
        if process.end_time == -1:
            process.end_time = run_for
        # Calculate the turnaround time for each process
        turnaround_times[process.name] = process.end_time - process.arrival
        wait_times[process.name] = turnaround_times[process.name] - process.burst

    return timeline, wait_times, response_times, turnaround_times

def srtf_scheduler(processes, run_for):
    timeline = []
    wait_times = {p.name: 0 for p in processes}
    response_times = {p.name: -1 for p in processes}
    turnaround_times = {p.name: 0 for p in processes}
    time = 0

    ready_queue = []
    processes.sort(key=lambda p: p.arrival)
    process_index = 0
    current_process = None

    while time < run_for:
        # Add newly arrived processes to the ready queue
        while process_index < len(processes) and processes[process_index].arrival == time:
            process = processes[process_index]
            heapq.heappush(ready_queue, (process.remaining, process.arrival, process))
            timeline.append(f"Time {time:>4} : {process.name} arrived")
            process_index += 1

        if current_process:
            current_process.remaining -= 1
            if current_process.remaining == 0:
                current_process.end_time = time
                timeline.append(f"Time {time:>4} : {current_process.name} finished")
                turnaround_times[current_process.name] = time - current_process.arrival
                current_process = None

        if not current_process and ready_queue:
            _, _, current_process = heapq.heappop(ready_queue)
            if current_process.start_time == -1:
                current_process.start_time = time
                response_times[current_process.name] = time - current_process.arrival
            timeline.append(f"Time {time:>4} : {current_process.name} selected (burst {current_process.remaining:>3})")

        if current_process:
            if ready_queue and ready_queue[0][0] < current_process.remaining:
                heapq.heappush(ready_queue, (current_process.remaining, current_process.arrival, current_process))
                _, _, current_process = heapq.heappop(ready_queue)
                if current_process.start_time == -1:
                    current_process.start_time = time
                    response_times[current_process.name] = time - current_process.arrival
                timeline.append(f"Time {time:>4} : {current_process.name} selected (burst {current_process.remaining:>3})")
        else:
            if not ready_queue and time < run_for:
                timeline.append(f"Time {time:>4} : Idle")

        time += 1

    for process in processes:
        if process.end_time == -1:
            process.end_time = run_for
        turnaround_times[process.name] = process.end_time - process.arrival
        wait_times[process.name] = turnaround_times[process.name] - process.burst

    return timeline, wait_times, response_times, turnaround_times

def round_robin_scheduler(processes, run_for, quantum):
    timeline = []
    wait_times = {p.name: 0 for p in processes}
    response_times = {p.name: -1 for p in processes}
    turnaround_times = {p.name: 0 for p in processes}

    time = 0
    ready_queue = deque()
    processes.sort(key=lambda p: p.arrival)  # Sort processes by arrival time
    process_index = 0
    current_process = None
    current_quantum = 0
    completed_processes = set()

    while time < run_for or ready_queue or current_process:
        # Add newly arrived processes to the ready queue
        while process_index < len(processes) and processes[process_index].arrival == time:
            process = processes[process_index]
            ready_queue.append(process)
            timeline.append(f"Time {time:>4} : {process.name} arrived")
            process_index += 1

        if current_process:
            current_process.remaining -= 1
            current_quantum += 1
            if response_times[current_process.name] == -1:
                response_times[current_process.name] = time - current_process.arrival - 1

            if current_process.remaining == 0:
                current_process.end_time = time
                timeline.append(f"Time {time:>4} : {current_process.name} finished")
                turnaround_times[current_process.name] = time - current_process.arrival
                completed_processes.add(current_process.name)
                current_process = None
                current_quantum = 0
            elif current_quantum == quantum:
                ready_queue.append(current_process)
                current_process = None
                current_quantum = 0

        if not current_process and ready_queue:
            current_process = ready_queue.popleft()
            if current_process.start_time == -1:
                current_process.start_time = time
            timeline.append(f"Time {time:>4} : {current_process.name} selected (burst {current_process.remaining:>3})")

        if not current_process and not ready_queue and process_index >= len(processes) and time < run_for:
            timeline.append(f"Time {time:>4} : Idle")
        
        time += 1

    # Calculate wait times
    for process in processes:
        if process.name not in completed_processes:
            turnaround_times[process.name] = time - process.arrival
        wait_times[process.name] = turnaround_times[process.name] - process.burst

    return timeline, wait_times, response_times, turnaround_times

def print_report(process_count, scheduling_type, quantum, timeline, wait_times, response_times, turnaround_times, run_for, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{process_count} processes\n")
        f.write(f"Using {scheduling_type}\n")
        if scheduling_type == 'Round-Robin':
            f.write(f"Quantum {quantum:>3}\n\n")
        for event in timeline:
            f.write(event + '\n')
        
        f.write(f"Finished at time {run_for:>3}\n\n")
        
        for name in wait_times:
            f.write(f"{name} wait {wait_times[name]:>3} turnaround {turnaround_times[name]:>3} response {response_times[name]:>3}\n")

def main(file):
    process_count, run_for, scheduling_type, quantum, processes = parse_input(file)
    if scheduling_type == 'fcfs':
        timeline, wait_times, response_times, turnaround_times = fcfs_scheduler(processes, run_for)
    elif scheduling_type == 'sjf':
        timeline, wait_times, response_times, turnaround_times = srtf_scheduler(processes, run_for)
    elif scheduling_type == 'rr':
        scheduling_type = 'Round-Robin'
        timeline, wait_times, response_times, turnaround_times = round_robin_scheduler(processes, run_for, quantum)
    else:
        raise ValueError("Unknown scheduling type")
    
    output_file = file.replace(".in", ".out")
    print_report(process_count, scheduling_type, quantum, timeline, wait_times, response_times, turnaround_times, run_for, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a CPU scheduler.")
    parser.add_argument("filename", help="The input file containing process information with a .in extension.")
    args = parser.parse_args()
    
    main(args.filename)
