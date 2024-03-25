import logging
from .rest_adapter import RestAdapter
from .models import *

test1 = RestAdapter()
# result = test1.get("/stops/60158")
# save = Stops(**result.data)
# print(save.WheelchairAccess)

result2 = test1.get("/stops/60158/estimates")
# save2 = StopEstimate(**result2.data)
bus_list = []
for d in result2.data:
    bus_list.append(StopEstimate(**d))

# To-do: This should be an object
next_bus = bus_list[0].Schedules[0]
# print(type(bus_list[0]))
print(next_bus.ExpectedCountdown)