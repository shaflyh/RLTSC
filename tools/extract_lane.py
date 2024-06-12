import xml.etree.ElementTree as ET
import csv
import os

def extract_lane_lengths(net_xml_path):
    # Load the XML file
    tree = ET.parse(net_xml_path)
    root = tree.getroot()

    # Dictionary to store lane lengths
    lane_lengths = []

    # Iterate through all edges in the network
    for edge in root.findall('edge'):
        # Ignore internal edges which are typically used in junction modeling
        if edge.get('function') == 'internal':
            continue

        # Iterate through each lane in the edge
        for lane in edge.findall('lane'):
            lane_id = lane.get('id')
            lane_length = float(lane.get('length'))
            lane_lengths.append([lane_id, lane_length])

    return lane_lengths

def write_to_csv(lane_lengths, output_file):
    # Write data to a CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['lane_id', 'length'])
        writer.writerows(lane_lengths)

def get_output_filename(net_xml_path):
    directory = os.path.dirname(net_xml_path)
    # Generate the output filename based on the input file name
    base_name = os.path.basename(net_xml_path)
    name_without_extension = base_name[:-8]  # remove '.net.xml'
    output_filename = f"{name_without_extension}_lane_lengths.csv"
    return os.path.join(directory, output_filename)

# Path to your .net.xml file
net_xml_file_path = './environments/ingolstadt21/ingolstadt21.net.xml'

# Generate the output CSV file name
output_csv_file_path = get_output_filename(net_xml_file_path)

# Extract lane lengths
lane_lengths = extract_lane_lengths(net_xml_file_path)

# Write the lane lengths to CSV
write_to_csv(lane_lengths, output_csv_file_path)

print(f"Data has been written to {output_csv_file_path}")
