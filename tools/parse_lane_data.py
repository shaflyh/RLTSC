import xml.etree.ElementTree as ET
import csv
import os

# Path to your .net.xml file
# xml_file_path = 'tools/data/Jakarta Blocked3.xml'
xml_file_paths = ['tools/data/Standard agent test.xml', 'tools/data/Robust agent test.xml', 'tools/data/Standard agent PGD attack.xml', 'tools/data/Robust agent PGD attack.xml']

def parse_xml_to_csv(xml_data, csv_filename):
    # Parse the XML data
    root = ET.parse(xml_data)
    total_flow = 0
    max_flow = 0
    peak_flow = 0
    # Prepare to write to a CSV file
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['time', 'lane_id', 'laneDensity', 'outflow'])

        # Iterate over each interval in the XML data
        for interval in root.findall('interval'):
            begin_time = interval.get('begin')
            flow_interval = 0

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
                    # outflow = arrived + left
                    total_flow = total_flow + outflow
                    flow_interval = flow_interval + outflow
                    peak_flow = max(peak_flow, outflow)

                    # Write to CSV
                    writer.writerow([begin_time, lane_id, lane_density, outflow])
            
            max_flow =  max(max_flow, flow_interval)
    print(f'Throughput : {total_flow}')
    print(f'Max flow: {max_flow}')
    print(f'Peak flow: {peak_flow}')

def get_output_filename(net_xml_path):
    directory = (os.path.dirname(net_xml_path))
    # Generate the output filename based on the input file name
    base_name = os.path.basename(net_xml_path)
    name_without_extension = base_name[:-4]  # remove '.xml'
    output_filename = f"{name_without_extension}.csv"
    return os.path.join(directory, output_filename)


# Generate the output CSV file name
for path in xml_file_paths:
    output_csv_file_path = get_output_filename(path)    
    print(output_csv_file_path)
    parse_xml_to_csv(path, output_csv_file_path)

    print(f"Data has been written to {output_csv_file_path}")
