# import requests

# GRAPHOPPER_API_KEY = "ef848d5d-2148-41ba-a188-5a91c039a94f"

# # 1. Yo'nalish chizish (Routing API)
# def get_route(driver_coords, customer_coords):
#     url = "https://graphhopper.com/api/1/route"
#     params = {
#         "key": GRAPHOPPER_API_KEY,
#         "point": [f"{driver_coords[0]},{driver_coords[1]}", f"{customer_coords[0]},{customer_coords[1]}"],
#         "vehicle": "car",
#         "instructions": "true",
#         "calc_points": "true"
#     }
#     response = requests.get(url, params=params)
#     return response.json()

# # 2. Masofa hisoblash (Matrix API)
# def get_distance_matrix(driver_coords, customer_coords):
#     url = "https://graphhopper.com/api/1/matrix"
#     payload = {
#         "key": GRAPHOPPER_API_KEY,
#         "points": [driver_coords, customer_coords],
#         "vehicle": "car",
#         "out_arrays": ["distances", "times"]
#     }
#     response = requests.post(url, json=payload)
#     return response.json()

# # Test uchun malumotlar
# driver_location = [41.2995, 69.2401]  # Toshkent, O'zbekiston
# customer_location = [41.3111, 69.2797]  # Toshkent markazi

# route_data = get_route(driver_location, customer_location)
# matrix_data = get_distance_matrix(driver_location, customer_location)

# print("Route Data:", route_data)
# print("Matrix Data:", matrix_data)


# import requests

# URL = "http://127.0.0.1:8000/api/v1/users/5555/18032007/"

# get = requests.get(URL).json()
# print(get)