import sys, csv
from lib import send_request

if __name__ == '__main__':
    data = send_request(sys.argv[1], sys.argv[2])
    buses = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    
    with open(sys.argv[3], 'wb') as f:
        csvwriter = csv.writer(f)
        
        csvwriter.writerow(["Latitude", "Longitude", "Stop Name", "Stop Status"])
        
        for bus in buses:
            if type(bus) != dict:
                continue
            bus = bus['MonitoredVehicleJourney']
            call = bus['OnwardCalls']['OnwardCall'][0] if len(bus['OnwardCalls']) else None
            
            csvwriter.writerow([
                bus['VehicleLocation']['Latitude'], 
                bus['VehicleLocation']['Longitude'],
                call['StopPointName'] if call else "N/A",
                call['Extensions']['Distances']['PresentableDistance'] if call else "N/A"
            ])