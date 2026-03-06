import requests
import json
import folium

'''
    Takes a list of waypoints (longitude, latitude)
    and returns routing information from OSRM, including distance and duration for each route. 
'''
def get_route_osrm(waypoints, alternatives=2):
    # Build coordinate string from waypoints list
    coords = ";".join([f"{lon},{lat}" for lon, lat in waypoints])
    
    url = f"https://router.project-osrm.org/route/v1/driving/{coords}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
        "alternatives": alternatives
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError(f"Routing failed: {data}")

    return data

'''
    Use folioum to plot the routes returned by OSRM on an interactive map. Each route will be displayed as a blue line.
'''
def plot_osrm_routes(data, out_file = None):
    if not data.get("routes"):
        print("No routes found to plot.")
        return

    # Get the first route's geometry for centering the map
    first_route = data["routes"][0]
    first_coords = first_route["geometry"]["coordinates"]
    center_lat = sum(lat for lon, lat in first_coords) / len(first_coords)
    center_lon = sum(lon for lon, lat in first_coords) / len(first_coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    for route in data["routes"]:
        coords = route["geometry"]["coordinates"]
        folium.PolyLine(locations=[(lat, lon) for lon, lat in coords], color="blue", weight=5).add_to(m)

    # Save the map to an HTML file
    if out_file:
        m.save(out_file)
    return m

'''
    Plot the OSRM routes on a map and overlay a circle representing the disaster area.
'''
def plot_osrm_routes_with_disaster(data, disaster_location, disaster_radius, out_file):
    m = plot_osrm_routes(data)

    # Add a circle to represent the disaster area
    folium.Circle(
        location=[disaster_location[1], disaster_location[0]],  # lat, lon
        radius=disaster_radius,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.5,
        popup='Disaster Area'
    ).add_to(m)

    m.save(out_file)

    return m


'''
    Check if a route crosses a disaster area defined by a center point and radius.
'''
def route_crosses_disaster_area(route, disaster_location, disaster_radius):
    for lon, lat in route["geometry"]["coordinates"]:
        distance = ((lon - disaster_location[0]) ** 2 + (lat - disaster_location[1]) ** 2) ** 0.5
        if distance <= disaster_radius:
            return True
    return False
