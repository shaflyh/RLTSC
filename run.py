import subprocess
import sys

import time
start_time = time.time()


def run_simulation_loop():
    # agents = ["MPLight", "IPPO"]
    # agents = ['STOCHASTIC', 'MAXWAVE', 'MAXPRESSURE', 'IDQN', 'IPPO', 'MPLight', 'MPLightFULL']
    # agents = ['IDQN1', 'IDQN2', 'IDQN3', 'IDQN4', 'IDQN5', 'IDQN6', 'IDQN1P', 'IDQN2P', 'IDQN3P', 'IDQN4P',
    #           'IDQN1PR', 'IDQN2PR', 'IDQN3PR', 'IDQN4PR', 'IDQN5PR', 'IDQN6PR', 'MPLight', 'MPLightFULL', 'MPLightR', 'MPLightFULLR']
    # agents = ['IDQN1', 'IDQN2', 'IDQN3', 'IDQN4', 'IDQN5', 'IDQN6', 'IDQN1P', 'IDQN2P', 'IDQN3P', 'IDQN4P',
    #           'IDQN1PR', 'IDQN2PR', 'IDQN3PR', 'IDQN4PR', 'IDQN5PR', 'IDQN6PR',
    #           'IPPO1', 'IPPO2', 'IPPO3', 'IPPO4', 'IPPO5', 'IPPO6', 'IPPO1P', 'IPPO2P', 'IPPO3P', 'IPPO4P',
    #           'IPPO1PR', 'IPPO2PR', 'IPPO3PR', 'IPPO4PR', 'IPPO5PR', 'IPPO6PR']
    agents = ['IDDQN1', 'IDDQN2', 'IDDQN3', 'IDDQN4', 'IDDQN5', 'IDDQN6', 'IDDQN1P', 'IDDQN2P', 'IDDQN3P', 'IDDQN4P',
              'IDDQN1PR', 'IDDQN2PR', 'IDDQN3PR', 'IDDQN4PR', 'IDDQN5PR', 'IDDQN6PR']
    agents = ['IDDQN1', 'IDDQN2', 'IDDQN3', 'IDDQN4', 'IDDQN5', 'IDDQN6', 'IDDQN1P', 'IDDQN2P', 'IDDQN3P', 'IDDQN4P']
    # maps = ['ingolstadt1', 'ingolstadt7', 'cologne1', 'cologne3', 'cologne8']
    maps = ['ingolstadt21', 'grid4x4', 'arterial4x4']

    for map_name in maps:
        print('map: ' + map_name)
        for agent in agents:
            print('agent: ' + agent)
            command = ["python", "-u", "main.py", "--agent", agent,
                       "--map", map_name]  # Add -u for unbuffered output

            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                for line in process.stdout:
                    print(line, end="")
        
                # Print the output and error (if any) for each map
                print(f"Output for {maps} {agent}:")
                print(process.stdout)
                print(f"Error for {maps} {agent}:")
                print(process.stderr)


# Start the simulation loop
run_simulation_loop()

# Total running time
end_time = time.time()
total_seconds = end_time - start_time
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print(
    f"All simulation time elapsed: {int(hours)} hours {int(minutes)} minutes {seconds:.2f}")
