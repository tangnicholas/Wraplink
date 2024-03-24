from typing import List, Dict

class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Stops:
    def __init__(self, StopNo: str, Name: str, City: str, OnStreet: str, AtStreet: str, Latitude: str, 
                 Longitude:str, WheelchairAccess:str, Distance: str, Routes: str):
        self.StopNo = StopNo
        self.Name = Name
        self.City = City
        self.OnStreet = OnStreet
        self.AtStreet = AtStreet
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.WheelchairAccess = WheelchairAccess
        self.Distance = Distance
        self.Routes = Routes
        pass