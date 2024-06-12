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
    return

def sjf_scheduler(processes, run_for):
    return

def round_robin_scheduler(processes, run_for, quantum):
    return

def print_report(process_count, scheduling_type, timeline, wait_times, response_times, turnaround_times, run_for, output_file):
    with open(output_file, 'w') as f:
        f.write(f"{process_count} processes\n")
        f.write(f"Using {scheduling_type}\n")
        for event in timeline:
            f.write(event + '\n')
        for time in range(run_for, run_for + (run_for - len(timeline))):
            f.write(f"Time {time}: Idle\n")
        f.write(f"Finished at time {run_for}\n")
        
        for name in wait_times:
            f.write(f"{name} wait {wait_times[name]} turnaround {turnaround_times[name]} response {response_times[name]}\n")

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
    
    output_file = file.replace(".in", ".out")
    print_report(process_count, scheduling_type, timeline, wait_times, response_times, turnaround_times, run_for, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a CPU scheduler.")
    parser.add_argument("filename", help="The input file containing process information with a .in extension.")
    args = parser.parse_args()
    
    main(args.filename)