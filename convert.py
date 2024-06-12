import subprocess

# List of map names
# map_names = ["ingolstadt21", "ingolstadt7", "ingolstadt1","arterial4x4"]
map_names = ["cologne1", "cologne3"]

# Loop through each map name
for map_name in map_names:
    # Define the command as a list of arguments
    command = ["python", "-u", "metrics/read.py", "--map", map_name]
    command2 = ["python", "-u", "metrics/graph.py", "--map", map_name]
    command3 = ["python", "-u", "metrics/summary.py", "--map", map_name]
    
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
    
    # Run the command
    # result = subprocess.run(command3, capture_output=True, text=True)
    with subprocess.Popen(command3, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        # Print standard output
        for line in process.stdout:
            print(line, end="")

        # Print standard error
        for line in process.stderr:
            print("Error:", line, end="")

        # Check if the process has exited with a non-zero status
        if process.returncode and process.returncode != 0:
            print(f"Command {' '.join(command)} failed with exit status {process.returncode}")