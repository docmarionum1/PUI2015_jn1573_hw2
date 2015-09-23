import sys
from lib import send_request

if __name__ == '__main__':
    # Make sure there are 2 parameters, if not exit
    if len(sys.argv) < 3:
        sys.exit("Usage: python show_bus_locations.py <apikey> <busroute>")

    # Send the API request with the API Key and Bus Route
    data = send_request(sys.argv[1], sys.argv[2])

    # Get to the list of buses
    buses = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

    print "Bus Line :", sys.argv[2]
    print "Number of Active Buses :", len(buses)

    for bus in buses:
        bus = bus['MonitoredVehicleJourney']
        print "%s is at latitude %s and longitude %s" % (bus['VehicleRef'],
            bus['VehicleLocation']['Latitude'], bus['VehicleLocation']['Longitude'])
