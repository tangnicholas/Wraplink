import logging
from .rest_adapter import RestAdapter
from .exceptions import TransLinkAPIError
from .models import *

class Wraplink:
    def __init__(self, hostname: str = 'api.translink.ca/rttiapi', api_key: str = 'RjxEAxso8GsoFzaXtLOn', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)

    def get_next_bus_arrivals(self, stop_num: int, get_count: int = -1, bus_num: int = -1) -> StopEstimate:
        endpoint_inst = f"/stops/{str(stop_num)}/estimates"
        
        filter_inst = ''
        if get_count != -1:
            filter_inst += f"&count={str(get_count)}"
        if bus_num != -1:
            filter_inst += f"&routeNo={str(bus_num)}"
            
        result = self._rest_adapter.get(endpoint=endpoint_inst, filter=filter_inst)

        bus_list = []
        for d in result.data:
            bus_list.append(StopEstimate(**d))
        
        nextbus = [] 
        for i in range(int(get_count)):
            nextbus.append(bus_list[0].Schedules[i].ExpectedLeaveTime)

        return nextbus
    

busapi = Wraplink()
result = busapi.get_next_bus_arrivals(stop_num= 61127, get_count= 3, bus_num= 33)
print(result)