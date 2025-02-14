import requests
from config import settings

GRAPH_HOPPER_API_URL = "https://graphhopper.com/api/1/route"

def get_route(driver_location, customer_location):
    """
    Haydovchidan mijozgacha bo‘lgan yo‘lni hisoblaydi.
    driver_location: (lat, lon)
    customer_location: (lat, lon)
    """
    params = {
        "point": [f"{driver_location[0]},{driver_location[1]}", f"{customer_location[0]},{customer_location[1]}"],
        "profile": "car",
        "locale": "en",
        "calc_points": True,
        "instructions": True,
        "key": settings.GRAPHHOPPER_API_KEY,
    }

    response = requests.get(GRAPH_HOPPER_API_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch route", "details": response.text}
