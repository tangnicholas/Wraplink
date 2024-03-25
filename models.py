from typing import List, Dict
from enum import Enum


class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []

class Stops:
    def __init__(self, StopNo: str, Name: str, BayNo: str, City: str, OnStreet: str, AtStreet: str, Latitude: float, 
                 Longitude: float, WheelchairAccess: int, Distance: float, Routes: str, **kwargs) -> None:
        self.StopNo = StopNo
        self.Name = Name
        self.BayNo = BayNo
        self.City = City
        self.OnStreet = OnStreet
        self.AtStreet = AtStreet
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.WheelchairAccess = WheelchairAccess
        self.Distance = Distance
        self.Routes = Routes
        self.__dict__.update(kwargs)

class ScheduleShort:
    ExpectedLeaveTime: str
    ExpectedCountdown: int
    ScheduleStatus: str
    LastUpdate: str

    def __init__(self, ExpectedLeaveTime: str, ExpectedCountdown: int, ScheduleStatus: str, LastUpdate: str, **kwargs) -> None:
        self.ExpectedLeaveTime = ExpectedLeaveTime
        self.ExpectedCountdown = ExpectedCountdown
        self.ScheduleStatus = ScheduleStatus
        self.LastUpdate = LastUpdate
        self.__dict__.update(kwargs)

class ScheduleFull(ScheduleShort):
    Destination: str
    CancelledTrip: bool
    CancelledStop: bool
    AddedTrip: bool
    AddedStop: bool

    def __init__(self, Destination: str, ExpectedLeaveTime: str, ExpectedCountdown: int, ScheduleStatus: str, CancelledTrip: bool, CancelledStop: bool, AddedTrip: bool, AddedStop: bool, LastUpdate: str, **kwargs) -> None:
        super().__init__(ExpectedLeaveTime, ExpectedCountdown, ScheduleStatus, LastUpdate)
        self.Destination = Destination
        self.CancelledTrip = CancelledTrip
        self.CancelledStop = CancelledStop
        self.AddedTrip = AddedTrip
        self.AddedStop = AddedStop
        self.__dict__.update(kwargs)

class StopEstimate:
    RouteNo: str
    RouteName: str
    Direction: str
    Schedules: List[ScheduleFull]

    def __init__(self, RouteNo: str, RouteName: str, Direction: str, Schedules: List[ScheduleShort] = None, **kwargs) -> None:
        self.RouteNo = RouteNo
        self.RouteName = RouteName
        self.Direction = Direction
        self.Schedules = [ScheduleFull(**s) for s in Schedules] if Schedules else []
        self.__dict__.update(kwargs)
