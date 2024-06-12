import sys
import argparse
import readXML
import readCSV

# Create an argument parser
parser = argparse.ArgumentParser(description="Read CSV and XML files for a given map.")
parser.add_argument("--map", required=True, help="The name of the map.")

# Parse the arguments
args = parser.parse_args()
map_name = args.map
# map_name = 'ingolstadt21'

readCSV.readCSV(map_name)
readXML.readXML(map_name)