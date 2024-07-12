import subprocess
import argparse

# List of map names
# map_names = ["ingolstadt21", "ingolstadt7", "ingolstadt1","arterial4x4"]
# maps = ['ingolstadt1', 'ingolstadt7', 'cologne1', 'cologne3', 'cologne8', 'jakarta']
# maps = ["ingolstadt1"]

# Create an argument parser
parser = argparse.ArgumentParser(description="Read CSV and XML files for a given map.")
parser.add_argument("--map", required=True, help="The name of the map.")
args = parser.parse_args()
maps = [args.map]

# Loop through each map name
for map in maps:
    # Define the command as a list of arguments
    command = ["python", "-u", "metrics/read.py", "--map", map]
    command2 = ["python", "-u", "metrics/graph.py", "--map", map]
    command3 = ["python", "-u", "metrics/summary.py", "--map", map]
    
    # Run the command
    # result = subprocess.run(command, capture_output=True, text=True)
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        # Print standard output
        for line in process.stdout:
            print(line, end="")

        # Print standard error
        for line in process.stderr:
            print("Error:", line, end="")

        # Check if the process has exited with a non-zero status
        if process.returncode and process.returncode != 0:
            print(f"Command {' '.join(command)} failed with exit status {process.returncode}")
    
    
    # Run the command
    # result = subprocess.run(command2, capture_output=True, text=True)
    with subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        # Print standard output
        for line in process.stdout:
            print(line, end="")

        # Print standard error
        for line in process.stderr:
            print("Error:", line, end="")

        # Check if the process has exited with a non-zero status
        if process.returncode and process.returncode != 0:
            print(f"Command {' '.join(command)} failed with exit status {process.returncode}")
    
    # # Run the command
    # with subprocess.Popen(command3, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
    #     # Print standard output
    #     for line in process.stdout:
    #         print(line, end="")

    #     # Print standard error
    #     for line in process.stderr:
    #         print("Error:", line, end="")

    #     # Check if the process has exited with a non-zero status
    #     if process.returncode and process.returncode != 0:
    #         print(f"Command {' '.join(command)} failed with exit status {process.returncode}")