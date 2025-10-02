"""Milestone 1"""

#Import standard library + requests
import requests #HTTP client to call Open-Meteo endpoints
from abc import ABC, abstractmethod #For abstract base classes
from typing import Tuple, Optional, Dict, Any #Type hints for clarity

#Custom Exceptions
class WeatherAPIError(Exception):
    """Base error for weatehr-related API failures"""
    pass

class LocationNotFoundError(WeatherAPIError):
    """No matches for given city/country"""
    pass

class InvalidDataError(WeatherAPIError):
    """API returns unexpected or invalid data"""
    pass

#Clean string
def sanitize_text(s: str) -> str:
    s = s.strip()
    s = " ".join(s.strip())
    return s

#Convert value to float
def to_float(name: str, value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        #If it doesn't work, raise InvalidDataError
        raise InvalidDataError(f"{name} must be a number.")

#Abstract base class
class Observation(ABC):
    """Abstract base class for any kind of observation"""
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Return JSON dictionary for this observation"""
        pass

class WeatherObservation(Observation):
    """Encapsulates a single weather reading with validated properties"""
    def __init__(
        self, 
        city: str, #City name
        country: str, #Country code
        latitude: float, #Latitude in degrees
        longitude: float, #Longitude in degrees
        temperature_c: float, #Temperature in celsius
        windspeed_kmh: float, #Wind speed in km/h
        observation_time: str, #Timestamp string
        notes: Optional[str] = None, #user note
    ) -> None:
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.temperature_c = temperature_c
        self.windspeed_kmh = windspeed_kmh
        self.observation_time = observation_time
        self.notes = notes

    #Encapsulated attributes, double underscore creates name-mangling
    __city: str
    __country: str
    __latitude: float
    __longitude: float
    __temperature_c: float
    __windspeed_kmh: float
    __observation_time: str
    __notes: Optional[str]

    #Properties with validation
    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, value: str) -> None:
        #Checking for non-empty string and sanitize
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("City must be a non-empty string")
        self.__city = sanitize_text(value)

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str) -> None:
        #Country is stored as 2-3 uppercase characters(country code)
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("Country must be a non-empty string")
        self.__country = sanitize_text(value).upper()

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, value: float) -> None:
        #Convert and validate range
        v = to_float("latitude", value)
        if not (-90.0 <= v <= 90.0):
            raise InvalidDataError("Latitude must be between -90 and 90")
        self.__latitude = v

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        #Convert and validate range
        v = to_float("Longitude", value)
        if not (-180.0 <= v <= 180.0):
            raise InvalidDataError("Longitude must be between -180 and 180")
        self.__longitude = v 

    @property
    def temperature_c(self) -> float:
        return self.__temperature_c

    @temperature_c.setter
    def temperature_c(self, value: float) -> None:
        #Convert and validate a reasonable temperature range
        v = to_float("Temperature_c", value)
        if not (-100.0 <= v <= 70.0):
            raise InvalidDataError("Temperature seems unrealistic")
        self.__temperature_c = v

    @property
    def windspeed_kmh(self) -> float:
        return self.__windspeed_kmh

    @windspeed_kmh.setter
    def windspeed_kmh(self, value: float) -> None:
        #Convert and can not be negative
        v = to_float("windspeed_kmh", value)
        if v < 0:
            raise InvalidDataError("Windspeed cannot be negative")
        self.__windspeed_kmh = v 

    @property
    def observation_time(self) -> str:
        return self.__observation_time

    @observation_time.setter
    def observation_time(self, value: str) -> None:
        #Non-empty string check
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("Observation time must be a non-empty string")
        self.__observation_time = sanitize_text(value)

    @property
    def notes(self) -> Optional[str]:
        return self.__notes

    @notes.setter
    def notes(self -> value: Optional[str]) -> None:
        #Allow None or sanitized string
        if value is None:
            self.__notes = None
        elif isinstance(value, str):
            self.__notes = sanitize_text(value)
        else:
            raise InvalidDataError("Notes must be a string or None")
    
    "Required by the abstract base class observation"
    def to_dict(self) -> Dict[str, Any]:
        #Return clean dictionary
        return {
            "city": self.city,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "temperature_c": self.temperature_c,
            "windspeed_kmh": self.windspeed_kmh,
            "observation_time": self.observation_time,
            "notes": self.notes,
        }
    
    #For printing quick debug lines
    def __repr__(self) -> str:
        #Representation of key fields
        return (
            "WeatherObservation("
            f"city={self.city!r}, country={self.country!r}, "
            f"lat={self.latitude:.4f}, lon={self.longitude:.4f} "
            f"tempC={self.temperature_c:.1f}, wind_kmh={self.windspeed_kmh:.1f} "
            f"time={self.observation_time!r}, notes={self.notes!r})"
        )