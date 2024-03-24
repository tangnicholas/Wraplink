from tilapya import RTTI
import time
from datetime import datetime


api = RTTI('RjxEAxso8GsoFzaXtLOn')
bus_stop_home = '61127'
bus_num_1 = '33'
last_updated = datetime.now()

def updateBusTime(bus_stop, bus_num):
    est = api.stop_estimates(bus_stop, count=3, route_number=bus_num)[0]
    busAPIrepsonse = [f'{sked.ExpectedLeaveTime}' for sked in est.Schedules]

    bus1 = busAPIrepsonse[0].isoformat(timespec='minutes')
    bus2 = busAPIrepsonse[1]
    bus3 = busAPIrepsonse[2]

    print(bus1)
    print(bus3)
    
    updateTimeLine(last_updated)

def updateTimeLine(last_updated):
    current_time = datetime.now()
    timeSinceLastUpdate = str(round((current_time - last_updated).total_seconds()))
    print("Last updated " + timeSinceLastUpdate + "s ago")
    

time.sleep(5)
updateBusTime(bus_stop_home, bus_num_1)





