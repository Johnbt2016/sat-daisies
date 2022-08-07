from pystac_client import Client
import rioxarray
import pyproj
import matplotlib.pyplot as plt
import numpy as np

api_url = "https://earth-search.aws.element84.com/v0"
client = Client.open(api_url)




def get_sat_images(datetime, lat, lon):

    collection = "sentinel-s2-l2a-cogs"
    # collection = 'landsat-8-l1-c1'

    geometry = {"type": "Point", "coordinates": (lon, lat)}
    
    mysearch = client.search(
        collections=[collection],
        intersects=geometry,
        max_items=50,
        datetime=datetime
    )


    items = mysearch.get_all_items()

    items_sorted = sorted(items, key=lambda x: x.properties["eo:cloud_cover"])

    return items_sorted[0]

def render_images(item, lat, lon, radius=10000, attribute_to_display = "visual"):
    proj = pyproj.Transformer.from_crs(4326, item.properties['proj:epsg'], always_xy=True)

    x1, y1 = (lon, lat)
    x2, y2 = proj.transform(x1, y1)
    assets = item.assets
    visual_href = assets[attribute_to_display].href
    visual = rioxarray.open_rasterio(visual_href)

    visual_clip = visual.rio.clip_box(minx=x2-radius,miny=y2-radius,maxx=x2+radius,maxy=y2+radius)
    print(item.datetime)
    if attribute_to_display == 'visual':
        visual_clip.plot.imshow(figsize=(10,10), cmap = 'viridis')
    else:
        # print(visual_clip['band'])
        visual_clipp = visual_clip.where(visual_clip.data == 6)
        print(np.nansum(visual_clipp.data))
    #     visual_clipp[0].plot.imshow(figsize=(10,10), cmap = 'viridis')
    plt.show()
    


if __name__ == "__main__":
    lat, lon = 37.0683, -111.2433 # Lake Powell

    # lat, lon = 39.6125, -106.0452 # Dillon reservoir
    # lat, lon = 41.1610, -112.5058 # great Salt lake
    # lat, lon = 39.0994, -120.0316 # Lake Tahoe
    # lat, lon = 40.2115, -111.8085 # Lake Utah, UT
    # lat, lon = 40.1787, -111.1261 # Strawberry reservoir, UT
    # lat, lon = 35.4268, -114.6385 # Lake Mohave, NE
    # lat, lon = 36.1465, -114.4232 # Lake Mead
    lat, lon = 35.7477, -120.9296 # Lake Nacimiento, CA # +++
    lat, lon = 38.2215, -120.9800 # Camanche reservoir, CA # +++
    lat, lon = 38.1545, -120.7988 # New Hogan Lake, CA # ++
    lat, lon = 37.9901, -120.5271 # New melones Lake, CA # +++
    lat, lon = 37.7165, -120.3899 # Don Pedro Reservoir, CA # -
    lat, lon = 43.7697, 6.1868 # Verdon Reservoir, France # +
    lat, lon = 43.9095, 6.5364 # Lac de Castillon, France #
    lat, lon = 43.9459, 6.5191, #Nord du lac de castillon, France
    lat, lon = 37.8190, -121.7348 # Los Vaqueros reservoir, CA +++
    lat, lon = 39.6931, -105.4325 # Beaver Brook reservoir, CO  
    lat, lon = 40.1542, -105.8519 # Lake Granby, CO, ++
    lat, lon = 41.2394, -101.7777 # McConaughy Lake, NB, +++


    for year in [2018, 2019, 2020, 2021, 2022]:
        for month in ['05', '10']:
            if month == '05':
                datetime=f"{year}-05-01/{year}-07-30"
            else:
                datetime=f"{year}-10-01/{year}-12-30"
            print(datetime)
            try:
                item = get_sat_images(datetime, lat, lon)
                render_images(item, lat, lon, radius=8000, attribute_to_display = "visual")
            except Exception as e:
                print(e)
                print(f"Nothing found for year {year} and month {month}")
                continue