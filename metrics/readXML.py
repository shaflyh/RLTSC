import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET

import numpy as np
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.map_config import map_configs
import matplotlib
matplotlib.use('TkAgg')

def count_episode(directory):
    with os.scandir(directory) as entries:
        return sum(1 for entry in entries if entry.is_file())

def readXML(map_name):    
    log_dir = os.path.join('process_results', map_name)
    print(log_dir)

    run_results = [folder for folder in next(os.walk(log_dir))[1]]

    metrics = ['timeLoss', 'duration', 'waitingTime']

    for metric in metrics:
        output_dir = os.path.join('metrics', map_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f'avg_{metric}.py')
        run_avg = dict()

        for run_name in run_results:
            print(f'Reading tripinfo {run_name}')
            split_name = run_name.split('-')
            map_name = map_name
            average_per_episode = []
            tripinfo_folder = os.path.join(log_dir, run_name, 'tripinfo')
            episodes = count_episode(tripinfo_folder)
        
            for i in range(1, episodes+1):
                trip_file = os.path.join(tripinfo_folder, f'tripinfo_{i}.xml')
                try:
                    print(i)
                    tree = ET.parse(trip_file)
                    root = tree.getroot()
                    num_trips, total = 0, 0.0
                    last_departure_time = 0
                    last_depart_id = ''
                    for child in root:
                        try:
                            num_trips += 1
                            total += float(child.attrib[metric])
                            if metric == 'timeLoss':
                                total += float(child.attrib['departDelay'])
                                depart_time = float(child.attrib['depart'])
                                if depart_time > last_departure_time:
                                    last_departure_time = depart_time
                                    last_depart_id = child.attrib['id']
                        except Exception as e:
                            print(e)
                            break

                    if metric == 'timeLoss':    # Calc. departure delays
                        route_file = os.path.join(
                            'environments', map_name, f'{map_name}.rou.xml')
                        if not os.path.exists(route_file):
                            route_file = os.path.join(
                                'environments', map_name, f'{map_name}_{i}.rou.xml')
                        tree = ET.parse(route_file)
                        root = tree.getroot()
                        last_departure_time = None
                        for child in root:
                            if child.attrib['id'] == last_depart_id:
                                # Get the time it was suppose to depart
                                last_departure_time = float(
                                    child.attrib['depart'])
                        never_departed = []
                        if last_departure_time is None:
                            raise Exception('Wrong trip file')
                        for child in root:
                            if child.tag != 'vehicle':
                                continue
                            depart_time = float(child.attrib['depart'])
                            if depart_time > last_departure_time:
                                never_departed.append(depart_time)
                        never_departed = np.asarray(never_departed)
                        never_departed_delay = np.sum(
                            float(map_configs[map_name]['end_time']) - never_departed)
                        total += never_departed_delay
                        num_trips += len(never_departed)

                    average = total / num_trips
                    average_per_episode.append(average)
                except ET.ParseError as e:
                    raise (e)
                    break

            # run_name = split_name[0]+' '+split_name[2]+' '+split_name[3]+' '+split_name[4]
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
                out.write("'{}': {},\n".format(alg_name[i], res.tolist()))
            out.write("}")
