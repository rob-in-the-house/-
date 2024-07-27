import requests
import numpy as np
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic
import web
import folium
from folium import GeoJson
from folium.plugins import MeasureControl
import random

def generate_grid_points(polygon_coords, spacing_km):
    # Create a Shapely polygon
    polygon = Polygon(polygon_coords)
    
    # Get the bounds of the polygon
    minx, miny, maxx, maxy = polygon.bounds
    
    # Convert spacing from km to degrees roughly
    spacing_deg = spacing_km / 111.32  # 1 degree ≈ 111.32 km
    
    # Generate grid points
    x_points = np.arange(minx, maxx, spacing_deg)
    y_points = np.arange(miny, maxy, spacing_deg)
    
    grid_points = []
    for x in x_points:
        for y in y_points:
            point = Point(x, y)
            if polygon.contains(point):
                grid_points.append((x, y))
    
    return grid_points

# def is_in_polygon(point, polygon):
#     point = Point(point)
#     polygon = Polygon(polygon)
#     return polygon.contains(point)


def gen_coords(area_code, distance=5):
    all_points = set()
    rep = requests.get(url='https://geo.datav.aliyun.com/areas_v3/bound/%s_full.json' % area_code)
    data = rep.json()
    for area in data['features']:
        polygon = area['geometry']['coordinates'][0][0]
        grid = generate_grid_points(polygon, distance)
        for point in grid:
            all_points.add(point)
    print(len(all_points))
    with open('%s.txt' % area_code, 'w') as fw:
        for point in all_points:
            fw.write("%s,%s\n" % point)    
    return all_points
    

def draw_polygon_points(zoom, area_code, distance):
    url = "https://geo.datav.aliyun.com/areas_v3/bound/geojson?code=%s" % area_code
    geo_json_data = requests.get(url).json()

    loc_set = gen_coords(area_code, distance)
    index = int(len(loc_set)/2)
    y,x = list(loc_set)[index]
    center = x,y
    map = folium.Map(location=center, zoom_start=zoom)
    map.add_child(
        folium.ClickForLatLng(format_str='lng + "," + lat', alert=True)
    )
    map.add_child(MeasureControl())
    GeoJson(geo_json_data, zoom_on_click=False).add_to(map)

    for loc in loc_set:
        print(loc)
        folium.Marker(location=[loc[1], loc[0]], popup='').add_to(map)
    map.save("map.html")

def render_map(html):
    with open(html) as f:
        return f.read()

class polygon:
    def GET(self):
        data = web.input()
        zoom = data.zoom if 'zoom' in data else 12
        code = data.code
        distance = data.distance if 'distance' in data else 5
        draw_polygon_points(zoom, data.code, float(distance))
        return render_map('map.html')

class data:
    def GET(self):
        data = web.input()
        code = data.code
        distance = data.distance if 'distance' in data else 5
        draw_polygon_points(12, data.code, float(distance))
        return open('%s.txt' % code, 'r').read()

urls = (
    '/polygon', 'polygon',
    '/data', 'data'
)
# gen_coords('650200')
if __name__ == "__main__":
    web.config.debug = False
    web.config.port = 8080
    web.config.host = '0.0.0.0'
    app = web.application(urls, globals())
    app.run()