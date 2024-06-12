# This program will read CSV results and write it to avg_queue.py

import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import matplotlib
matplotlib.use('TkAgg')


def readCSV(map_name):
    episodes = 100
    log_dir = os.path.join('results', map_name)
    print(log_dir)
    run_results = [folder for folder in next(os.walk(log_dir))[1]]

    metric = 'queue'
    output_dir = os.path.join('metrics', map_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, f'avg_{metric}.py')
    run_avg = dict()

    for run_name in run_results:
        print(f'Reading metric {run_name}')
        # split_name = run_name.split('-')
        average_per_episode = []
        for i in range(1, episodes+1):
            metric_file = os.path.join(
                log_dir, run_name, 'metrics', f'metrics_{i}.csv')
            if not os.path.exists(metric_file):
                raise FileNotFoundError(f"{metric_file} does not exist!")

            num_steps, total = 0, 0.0
            last_departure_time = 0
            last_depart_id = ''
            with open(metric_file) as fp:
                reward, wait, steps = 0, 0, 0
                for line in fp:
                    line = line.split('}')
                    queues = line[2]
                    signals = queues.split(':')
                    step_total = 0
                    # Sum value in one line
                    for s, signal in enumerate(signals):
                        if s == 0:
                            continue
                        queue = signal.split(',')
                        queue = int(queue[0])
                        step_total += queue
                    # Get the average for one time step
                    # add -1 because of excluding the first line
                    step_avg = step_total / (len(signals)-1)
                    total += step_avg
                    num_steps += 1

            # Get the average for one episode
            average = total / num_steps
            average_per_episode.append(average)

        # run_name = split_name[0]+' '+split_name[2]+' ' + \
        #     split_name[3]+' '+split_name[4]
        # if len(split_name) > 5:
        #     run_name += ' '+split_name[5]
        average_per_episode = np.asarray(average_per_episode)

        # Always add new key even the method name is same
        run_avg[run_name] = [average_per_episode]
        # if run_name in run_avg:
        #     run_avg[run_name].append(average_per_episode)
        # else:
        #     run_avg[run_name] = [average_per_episode]

    alg_res = []
    alg_name = []
    for run_name in run_avg:
        list_runs = run_avg[run_name]
        min_len = min([len(run) for run in list_runs])
        list_runs = [run[:min_len] for run in list_runs]
        avg_delays = np.sum(list_runs, 0)/len(list_runs)
        err = np.std(list_runs, axis=0)

        alg_name.append(run_name)
        alg_res.append(avg_delays)

        alg_name.append(run_name+'_yerr')
        alg_res.append(err)

        plt.title(run_name)
        plt.plot(avg_delays)
        # plt.show()

    np.set_printoptions(threshold=sys.maxsize)
    with open(output_file, 'w') as out:
        out.write(f'{metric} = {{')
        for i, res in enumerate(alg_res):
            out.write(f"'{alg_name[i]}': {res.tolist()},\n")
        out.write("}")
