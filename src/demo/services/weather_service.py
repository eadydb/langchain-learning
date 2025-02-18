"""Weather service module."""
from typing import List
from ..schemas.base import WeatherResponse

class WeatherService:
    """Service for weather-related operations."""
    
    @staticmethod
    def get_current_weather(location: str, unit: str = "celsius") -> WeatherResponse:
        """
        Get the current weather for a location.
        
        Args:
            location: The location to get weather for
            unit: Temperature unit (celsius/fahrenheit)
            
        Returns:
            WeatherResponse: Weather data
        """
        # Mock weather data
        return WeatherResponse(
            location=location,
            temperature="22",
            unit=unit,
            forecast=["sunny", "windy"]
        )
