import matplotlib.pyplot as plt
import numpy as np
import importlib
from collections import deque
import argparse
import os

# Create an argument parser
parser = argparse.ArgumentParser(description="Read CSV and XML files for a given map.")
parser.add_argument("--map", required=True, help="The name of the map.")
parser.add_argument("--show", action='store_true', help="Show plot.")

# Parse the arguments
args = parser.parse_args()
map_name = args.map

save_dir = os.path.join('metrics', map_name)

timeLoss = importlib.import_module(f'{map_name}.avg_timeLoss').timeLoss
duration = importlib.import_module(f'{map_name}.avg_duration').duration
waitingTime = importlib.import_module(f'{map_name}.avg_waitingTime').waitingTime
queue = importlib.import_module(f'{map_name}.avg_queue').queue

method_list = {
    'FIXED': 'Fixed Time',
    'STOCHASTIC': 'Random',
    'MAXWAVE': 'Greedy',
    'MAXPRESSURE': 'Max Pressure',
    'FULLMAXPRESSURE': 'Max Pressure w/ All phases',
    'IDQN': 'IDQN',
    'IDDQN': 'IDDQN',
    'IDDQN2': 'IDDQN2',
    'IDQN2': 'IDQN2',
    'MPLight': 'MPLight',
    'MPLightFULL': 'Full State MPLight',
    'FMA2C': 'FMA2C',
    'IPPO': 'IPPO'
}

statics = ['MAXPRESSURE', 'STOCHASTIC', 'MAXWAVE', 'FIXED']

num_n = -1
num_episodes = 100
fs = 21
window_size = 5

metrics_data = [queue, timeLoss, duration, waitingTime]
metrics_name = ['Average Queue', 'Average Delay',
                'Average Trip Time', 'Average Wait']

chart = {
    'IDQN': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'IDDQN': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'IDDQN2': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'IDQN2': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'IPPO': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'MPLight': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'FMA2C': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
    'Full State MPLight': {
        'Average Queue': [],
        'Average Delay': [],
        'Average Wait': [],
        'Average Trip Time': []
    },
}


for met_i, metric_data in enumerate(metrics_data):
    # print('\n--------------------------')
    # print(f'Metrics: {metrics_name[met_i]}')
    # print()
    dqn_max = 0
    descs = []
    plt.gca().set_prop_cycle(None)
    # plt.figure(figsize=(8, 4)) 
    plt.figure(figsize=(10, 6))  # Set the figure size
    for run_name in metric_data:
        # print(f'\nResult: {run_name}')
        if '_yerr' not in run_name:
            method_name = run_name.split('-')[0]
            state_name = run_name.split('-')[1]
            reward_name = run_name.split('-')[2]
            desc = (run_name.split('-')[3])
            label_name = f'{method_name} {state_name} {reward_name}'
            
            # print('---------------------')
            # print('method: ' + method_name)
            # print('map: ' + map_name)
            # print('state: ' + state_name)
            # print('reward: ' + reward_name)

            if method_name == 'IDQN' or method_name == 'IDDQN':
                # Set ylim to DQN max, it's approx. random perf.
                dqn_max = np.max(metric_data[run_name])

            # Fixed time isn't applicable to valid. scenario, skip color for consistency
            if len(metric_data[run_name]) == 0:
                plt.plot([], [])
                plt.fill_between([], [], [])
                continue

            # Print out performance metric
            err = metric_data.get(run_name + '_yerr')
            if num_n == -1:
                last_n_ind = np.argmin(metric_data[run_name])
                last_n = metric_data[run_name][last_n_ind]
            else:
                last_n_ind = np.argmin(metric_data[run_name][-num_n:])
                last_n = metric_data[run_name][-num_n:][last_n_ind]
            last_n_err = 0 if err is None else err[last_n_ind]
            avg_tot = np.mean(metric_data[run_name])
            avg_tot = np.round(avg_tot, 2)
            last_n = np.round(last_n, 2)
            last_n_err = np.round(last_n_err, 2)

            # last_n = np.round(np.mean(err), 2) if err is not None else 0
            # last_n = last_n_ind

            # Print stats
            if method_name in statics:
                # print('{} {}'.format(method_list[method_name], avg_tot))
                do_nothing = 0
            else:
                # print(
                #     '{} {} +- {}'.format(method_list[method_name], last_n, last_n_err))
                if not (map == 'grid4x4' or map == 'arterial4x4'):
                    chart[method_list[method_name]][metrics_name[met_i]].append(
                        str(last_n))  # +' $\pm$ '+str(last_n_err)

            # Build plots
            if method_name in statics:
                plt.plot([avg_tot]*num_episodes,
                            '--', label=method_list[method_name])
                plt.fill_between([], [], [])      # Advance color cycle
            # elif not ('FMA2C' in method_name or 'IPPO' in method_name):
            elif not ('FMA2C' in method_name in method_name):
                windowed = []
                queue = deque(maxlen=window_size)
                std_q = deque(maxlen=window_size)

                windowed_yerr = []
                x = []
                for i, eps in enumerate(metric_data[run_name]):
                    x.append(i)
                    queue.append(eps)
                    windowed.append(np.mean(queue))
                    if err is not None:
                        std_q.append(err[i])
                        windowed_yerr.append(np.mean(std_q))

                windowed = np.asarray(windowed)
                if err is not None:
                    windowed_yerr = np.asarray(windowed_yerr)
                    low = windowed - windowed_yerr
                    high = windowed + windowed_yerr
                else:
                    low = windowed
                    high = windowed
                # print(windowed)
                plt.plot(windowed, label=desc, linewidth=2)
                plt.fill_between(x, low, high, alpha=0.4)
            else:
                if method_name == 'FMA2C':  # Skip pink in color cycle
                    plt.plot([], [])
                    plt.fill_between([], [], [])
                # method_name = run_name.split(' ')[0]
                x = [num_episodes-1, num_episodes]
                y = [last_n]*2
                # plt.plot(x, y, label=method_list[method_name])
                plt.plot(x, y, label=descs, color='b', linewidth=2)
                plt.fill_between([], [], [])  # Advance color cycle

    points = np.asarray([0, 20, 40, 60, 80, 100, num_episodes])
    # labels = ('0', '20', '40', '60', '80', '100', '..1400')
    plt.yticks()
    # plt.xticks(points, labels)
    plt.xlabel('Episode', fontsize=14)
    plt.ylabel(metrics_name[met_i], fontsize=14)
    # plt.ylabel('Delay (s)')
    # plt.title(
    #     f'{metrics_name[met_i]} {graph_map_title[map]}')
    plt.title(metrics_name[met_i] + ' Over Episodes', fontsize=16)
    # plt.tight_layout(rect=[0, 0, 0.6, 1]) 
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(fontsize=12)
    plt.tight_layout()
    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    bot, top = plt.ylim()
    if bot < 0:
        bot = 0
    # plt.ylim(0, dqn_max)
    file_path = os.path.join(save_dir, metrics_name[met_i] + '.png')
    plt.savefig(file_path, dpi=300)
    # print(args.show)
    # is_show = False
    if args.show:
        plt.show()
    else:
        plt.clf()

# for method_name in chart:
#     print(method_name)
#     for met in metrics_name:
#         print(met, ' & ', ' & '.join(chart[method_name][met]), '\\\\')
