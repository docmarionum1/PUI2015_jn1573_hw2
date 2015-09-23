import sys, csv
from lib import send_request

if __name__ == '__main__':
    # Make sure there are 3 parameters, if not exit
    if len(sys.argv) < 4:
        sys.exit("Usage: python get_bus_info.py <apikey> <busroute> <output_file>")

    # Send the API request with the API Key and Bus Route
    data = send_request(sys.argv[1], sys.argv[2])

    # Get to the list of buses
    buses = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

    with open(sys.argv[3], 'wb') as f:
        csvwriter = csv.writer(f)

        # Add the header
        csvwriter.writerow(["Latitude", "Longitude", "Stop Name", "Stop Status"])

        for bus in buses:
            bus = bus['MonitoredVehicleJourney']

            # Handle empty onward call
            call = bus['OnwardCalls']['OnwardCall'][0] if len(bus['OnwardCalls']) else None

            # Write the bus to the CSV handling missing onward call data
            csvwriter.writerow([
                bus['VehicleLocation']['Latitude'],
                bus['VehicleLocation']['Longitude'],
                call['StopPointName'] if call else "N/A",
                call['Extensions']['Distances']['PresentableDistance'] if call else "N/A"
            ])
