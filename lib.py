import sys
import tempfile
import time
import json
import requests
from os import path

URL = 'http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?VehicleMonitoringDetailLevel=calls&key=%s&LineRef=%s'
RATE_LIMIT = 30
CACHE_FILE_NAME = 'bustimecache'
CACHE_FILE = path.join(tempfile.gettempdir(), CACHE_FILE_NAME)

def send_request(apikey, busline):
    # Check if there is a cached copy and if so whether it is less than
    # 30 seconds old.  If so go to the cache.
    if use_cache(busline):
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
    else:
        response = requests.get(URL % (apikey, busline))
        data = response.json()
        
        # Make sure request was correct
        if 'ErrorCondition' in data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]:
            sys.exit('ERROR : ' + data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['ErrorCondition']['Description'])
            
        with open(CACHE_FILE, 'wb') as f:
            f.write(response.text)
            
    return data
    
def use_cache(busline):
    if not path.exists(CACHE_FILE):
        return False
    elif (time.time() - path.getmtime(CACHE_FILE)) > RATE_LIMIT:
        return False
        
    # Check if cached file matches requested Bus line
    with open(CACHE_FILE, 'r') as f:
        data = json.load(f)
        if data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][0]['MonitoredVehicleJourney']['PublishedLineName'] != busline:
            sys.exit("ERROR: %s does not match cached data.  Try again in %s seconds" % (busline, RATE_LIMIT - int(time.time() - path.getmtime(CACHE_FILE))))

    return True
        