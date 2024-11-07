import pandas as pd
import numpy as np
import time

# Load process data from the provided Excel file
data = pd.read_excel('processes.xlsx')
processes = data[['PID', 'arrival_time', 'Burst_time']].to_dict('records')

# FCFS Scheduling
def fcfs_schedule(processes):
    processes.sort(key=lambda x: x['arrival_time'])
    current_time = 0
    results = []
    for process in processes:
        start_time = max(current_time, process['arrival_time'])
        end_time = start_time + process['Burst_time']
        results.append({
            'ProcessID': process['PID'],
            'Start': start_time,
            'End': end_time
        })
        current_time = end_time
    return results

# SJF Non-Preemptive Scheduling
def sjf_non_preemptive_schedule(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['Burst_time']))
    current_time = 0
    results = []
    while processes:
        available_processes = [p for p in processes if p['arrival_time'] <= current_time]
        if not available_processes:
            current_time += 1
            continue
        shortest_job = min(available_processes, key=lambda x: x['Burst_time'])
        start_time = max(current_time, shortest_job['arrival_time'])
        end_time = start_time + shortest_job['Burst_time']
        results.append({
            'ProcessID': shortest_job['PID'],
            'Start': start_time,
            'End': end_time
        })
        current_time = end_time
        processes.remove(shortest_job)
    return results

# SJF Preemptive Scheduling
def sjf_preemptive_schedule(processes):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    remaining_times = {p['PID']: p['Burst_time'] for p in processes}
    results = []
    current_time = 0
    last_process = None
    while any(remaining_times.values()):
        available_processes = [p for p in processes if p['arrival_time'] <= current_time and remaining_times[p['PID']] > 0]
        if not available_processes:
            current_time += 1
            continue
        shortest_job = min(available_processes, key=lambda x: remaining_times[x['PID']])
        if last_process != shortest_job['PID']:
            start_time = current_time
        remaining_times[shortest_job['PID']] -= 1
        current_time += 1
        if remaining_times[shortest_job['PID']] == 0:
            results.append({
                'ProcessID': shortest_job['PID'],
                'Start': start_time,
                'End': current_time
            })
            last_process = None
        else:
            last_process = shortest_job['PID']
    return results

# LJF Preemptive Scheduling
def ljf_preemptive_schedule(processes):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    remaining_times = {p['PID']: p['Burst_time'] for p in processes}
    results = []
    current_time = 0
    last_process = None
    while any(remaining_times.values()):
        available_processes = [p for p in processes if p['arrival_time'] <= current_time and remaining_times[p['PID']] > 0]
        if not available_processes:
            current_time += 1
            continue
        longest_job = max(available_processes, key=lambda x: remaining_times[x['PID']])
        if last_process != longest_job['PID']:
            start_time = current_time
        remaining_times[longest_job['PID']] -= 1
        current_time += 1
        if remaining_times[longest_job['PID']] == 0:
            results.append({
                'ProcessID': longest_job['PID'],
                'Start': start_time,
                'End': current_time
            })
            last_process = None
        else:
            last_process = longest_job['PID']
    return results

# Round Robin Scheduling
def round_robin_schedule(processes, quantum=12):
    queue = []
    current_time = 0
    results = []
    remaining_times = {p['PID']: p['Burst_time'] for p in processes}
    queue.extend([p for p in processes if p['arrival_time'] <= current_time])
    arrived_processes = set(p['PID'] for p in queue)
    
    while queue or any(rt > 0 for rt in remaining_times.values()):
        if not queue:
            current_time += 1
            queue.extend([p for p in processes if p['arrival_time'] <= current_time and p['PID'] not in arrived_processes])
            arrived_processes.update(p['PID'] for p in queue)
            continue

        process = queue.pop(0)
        pid = process['PID']
        start_time = max(current_time, process['arrival_time'])
        execution_time = min(remaining_times[pid], quantum)
        end_time = start_time + execution_time
        results.append({
            'ProcessID': pid,
            'Start': start_time,
            'End': end_time
        })
        current_time = end_time
        remaining_times[pid] -= execution_time
        if remaining_times[pid] > 0:
            queue.extend([p for p in processes if p['arrival_time'] <= current_time and p['PID'] not in arrived_processes])
            queue.append(process)  # Re-add the process if it's not finished
            arrived_processes.update(p['PID'] for p in queue)
    return results

# Display results
def print_schedule_results(schedule_name, results, exec_time):
    print(f"\n{schedule_name} Schedule (Execution Time: {exec_time:.6f} seconds):")
    for result in results:
        print(f"Process {result['ProcessID']}: Start = {result['Start']}, End = {result['End']}")

# Prompt user for scheduling choice
print("Select a Scheduling Algorithm:")
print("1. First Come First Serve (FCFS)")
print("2. Shortest Job First (Non-Preemptive)")
print("3. Shortest Job First (Preemptive)")
print("4. Longest Job First (Preemptive)")
print("5. Round Robin (Quantum = 12)")
choice = input("Enter your choice (1-5): ")

# Measure execution time and display results
if choice == "1":
    start_time = time.time()
    results = fcfs_schedule(processes)
    exec_time = time.time() - start_time
    print_schedule_results("FCFS", results, exec_time)
elif choice == "2":
    start_time = time.time()
    results = sjf_non_preemptive_schedule(processes)
    exec_time = time.time() - start_time
    print_schedule_results("SJF Non-Preemptive", results, exec_time)
elif choice == "3":
    start_time = time.time()
    results = sjf_preemptive_schedule(processes)
    exec_time = time.time() - start_time
    print_schedule_results("SJF Preemptive", results, exec_time)
elif choice == "4":
    start_time = time.time()
    results = ljf_preemptive_schedule(processes)
    exec_time = time.time() - start_time
    print_schedule_results("LJF Preemptive", results, exec_time)
elif choice == "5":
    start_time = time.time()
    results = round_robin_schedule(processes)
    exec_time = time.time() - start_time
    print_schedule_results("Round Robin", results, exec_time)
else:
    print("Invalid choice. Please select a number between 1 and 5.")
