import matplotlib.pyplot as plt
import importlib
import argparse
import os
import pandas as pd
import numpy as np

# Create an argument parser
parser = argparse.ArgumentParser(
    description="Read CSV and XML files for a given map.")
parser.add_argument("--map", required=True, help="The name of the map.")

# Parse the arguments
args = parser.parse_args()
map_name = args.map

# List of attribute names
metrics = ['avg_timeLoss', 'avg_duration', 'avg_waitingTime', 'avg_queue']

# Dictionary to store the imported attributes
results = {}

# Loop through each attribute name and import the corresponding module
for attr in metrics:
    module = importlib.import_module(f'{map_name}.{attr}')
    # Extract the attribute name (e.g., 'timeLoss')
    attribute_name = attr.split('_')[1]
    results[attribute_name] = getattr(module, attribute_name)

# Name for state and reward in the excel summary
state_names = {
    'queue': 'Queue',
    'approach': 'Approach',
    'speed': 'Speed',
    'drq_norm': 'QAS',  # Queue + action + state
    # 'mplight': 'Pressure',
    # 'mplight_full': 'Full State',
    'queue_rand': 'Queue (Noise)',
    'drq_norm_rand': 'QAS (Noise)',
    # 'mplight_rand': 'Pressure (Noise)',
    # 'mplight_full_rand': 'Full State (Noise)',
}

rewards_names = {
    'pressure': 'Pressure',
    'wait_norm': 'Waiting Time',
    'pressure_rand': 'Pressure (Noise)',
}

df = pd.DataFrame(index=list(rewards_names.values()),
                  columns=list(state_names.values()))
# df_n = pd.DataFrame(index=list(rewards_names.values()),
#                     columns=list(state_names_noise.values()))

# print(results['avg_timeLoss'])

# Get maximum value for each average result
for metric, values in results.items():
    
    # Sort the dictionary keys
    sorted_keys = sorted(values.keys())
    # Create a new dictionary with the sorted keys
    sorted_values = {key: values[key] for key in sorted_keys}
    prev_algo = None
    min_average = {}
    for idx, (file_name, values) in enumerate(sorted_values.items()):
        if file_name[-5:] == "_yerr":
            continue
        
        print(file_name)
        min_average[file_name] = min(values)
        split = file_name.split('-')
        algorithm = split[0]
        state = split[1]
        reward = split[2]
        
        is_change = prev_algo is not None and prev_algo != algorithm
        
        if (is_change): # Check if it's the last iteration
            save_dir = os.path.join('metrics', map_name, f'{prev_algo}_min_{metric}.xlsx')
            df.to_excel(save_dir, engine='openpyxl')
            print('Result has been saved to ' + save_dir)
            df.loc[:, :] = np.nan
        
        prev_algo = algorithm
        df.at[rewards_names[reward], state_names[state]] = min(values)
    
    save_dir = os.path.join('metrics', map_name, f'{prev_algo}_min_{metric}.xlsx')
    df.to_excel(save_dir, engine='openpyxl')
    print('Result has been saved to ' + save_dir)
    df.loc[:, :] = np.nan
    

# Save the DataFrame to an Excel file
# save_dir = os.path.join('metrics', map_name, 'timeLoss.xlsx')
# save_dir2 = os.path.join('metrics', map_name, 'timeLossNoise.xlsx')
# df.to_excel(save_dir, engine='openpyxl')
# df_n.to_excel(save_dir2, engine='openpyxl')
# 

# # Print the result
# sorted_items = sorted(min_average.items(), key=lambda item: item[1])
# min_average.clear()
# min_average.update(sorted_items)

# for agent_name, min_value in min_average.items():
#     print(f"{agent_name}: {min_value}")
