import requests
import json
import folium

from utils.routing_functions import get_route_osrm, plot_osrm_routes, plot_osrm_routes_with_disaster, route_crosses_disaster_area

waypoints = [
    (2.3522, 48.8566),  # Paris
    (4.9041, 52.3676),  # Amsterdam
    (10.7522, 59.9139)  # Oslo
]

disatster_location = (10.0, 55.5)  # Odense, Denmark
disatster_radius = 100000  # 100 km

data = get_route_osrm(waypoints=waypoints)

# Check if any route is returned
print(f"Number of routes returned with waypoints: {len(data['routes'])}")
for i, route in enumerate(data["routes"], start=1):
    print(f"Route {i}: {route['distance']} meters, {route['duration']} seconds") 

# Plot the routes on an interactive map
map = plot_osrm_routes(data, out_file="assets/osrm_routes.html")

for i, route in enumerate(data["routes"], start=1):
    if route_crosses_disaster_area(route, disatster_location, disatster_radius):
        print(f"Route {i} crosses the disaster area.")
    else:
        print(f"Route {i} does NOT cross the disaster area.")

map = plot_osrm_routes_with_disaster(data, disatster_location, disatster_radius, out_file="assets/osrm_routes_with_disaster.html")
