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


new_list = [item.split('-')[-1] for item in list(results[attribute_name].keys())] 
print(new_list)
# df = pd.DataFrame(columns=list(state_names.values()))
df = pd.DataFrame(index=new_list,
                    columns=list(results.keys()))

print(df)
# print(results['avg_timeLoss'])

# Get maximum value for each average result
for metric, values in results.items():
    print(metric)
    # Sort the dictionary keys
    sorted_keys = sorted(values.keys())
    # Create a new dictionary with the sorted keys
    sorted_values = {key: values[key] for key in sorted_keys}
    prev_algo = None
    min_average = {}
    desc = ''
    for idx, (file_name, values) in enumerate(sorted_values.items()):
        if file_name[-5:] == "_yerr":
            continue
        
        print(file_name)
        # min_average[file_name] = min(values)
        min_average[file_name] = np.mean(values)
        split = file_name.split('-')
        algorithm = split[0]
        state = split[1]
        reward = split[2]
        desc = split[3]
        
        is_change = prev_algo is not None and prev_algo != algorithm
    
        # print(min_average[file_name])
        df.at[desc, metric] = np.mean(values)

print(df)
# Save the DataFrame to an Excel file
save_dir = os.path.join('metrics', map_name, 'summary.xlsx')
# save_dir2 = os.path.join('metrics', map_name, 'timeLossNoise.xlsx')
df.to_excel(save_dir, engine='openpyxl')
# df_n.to_excel(save_dir2, engine='openpyxl')
# 

# # Print the result
# sorted_items = sorted(min_average.items(), key=lambda item: item[1])
# min_average.clear()
# min_average.update(sorted_items)

# for agent_name, min_value in min_average.items():
#     print(f"{agent_name}: {min_value}")
