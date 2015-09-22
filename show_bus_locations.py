import sys
from lib import send_request

if __name__ == '__main__':
    data = send_request(sys.argv[1], sys.argv[2])
    buses = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    
    print "Bus Line :", sys.argv[2]
    print "Number of Active Buses :", len(buses) - 2 #Account for timestamps
    
    for bus in buses:
        if type(bus) != dict:
            continue
        bus = bus['MonitoredVehicleJourney']
        print "%s is at latitude %s and longitude %s" % (bus['VehicleRef'], 
            bus['VehicleLocation']['Latitude'], bus['VehicleLocation']['Longitude'])