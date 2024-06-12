import xml.etree.ElementTree as ET
import csv
import os

def parse_xml_to_csv(xml_data, csv_filename):
    # Parse the XML data
    root = ET.parse(xml_data)

    # Prepare to write to a CSV file
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['time', 'lane_id', 'laneDensity', 'outflow'])

        # Iterate over each interval in the XML data
        for interval in root.findall('interval'):
            begin_time = interval.get('begin')

            # Iterate over each edge within the interval
            for edge in interval.findall('edge'):
                # Iterate over each lane within the edge
                for lane in edge.findall('lane'):
                    lane_id = lane.get('id')
                    lane_density = lane.get('laneDensity', '0')  # Default density to '0' if not specified
                    departed = int(lane.get('departed', '0'))
                    arrived = int(lane.get('arrived', '0'))
                    entered = int(lane.get('entered', '0'))
                    left = int(lane.get('left', '0'))

                    # Calculate outflow
                    outflow = arrived + left * 12

                    # Write to CSV
                    writer.writerow([begin_time, lane_id, lane_density, outflow])
    print

def get_output_filename(net_xml_path):
    directory = os.path.dirname(os.path.dirname(net_xml_path))
    # Generate the output filename based on the input file name
    base_name = os.path.basename(net_xml_path)
    name_without_extension = base_name[:-4]  # remove '.xml'
    output_filename = f"{name_without_extension}.csv"
    return os.path.join(directory, output_filename)

# Path to your .net.xml file
xml_file_path = './results/ingolstadt7/IDQN-tr0-7-drq_norm-wait_norm/lanedata/lanedata_100.xml'

# Generate the output CSV file name
output_csv_file_path = get_output_filename(xml_file_path)    

parse_xml_to_csv(xml_file_path, output_csv_file_path)

print(f"Data has been written to {output_csv_file_path}")
