import pyproj
import rioxarray
import numpy as np
import pydaisi as pyd
import time

s2_utils = pyd.Daisi("laiglejm/S2 Utils")

def dummy():
    return 0

def download_band(item, band, lat, lon, radius=10000):
    proj = pyproj.Transformer.from_crs(4326, item.properties['proj:epsg'], always_xy=True)

    x1, y1 = (lon, lat)
    x2, y2 = proj.transform(x1, y1)
    assets = item.assets

    a = band
    visual_href = assets[a].href
    visual = rioxarray.open_rasterio(visual_href)
    visual_clip = visual.rio.clip_box(
                    minx=x2-radius,
                    miny=y2-radius,
                    maxx=x2+radius,
                    maxy=y2+radius
                )
    data = visual_clip.data[0]

    return data

def prepare_data(execs_ids):
    execs = [s2_utils.dummy() for _ in execs_ids]
    for i, e in enumerate(execs):
        e.id = execs_ids[i]

    status = [e.status for _ in execs]

    while "RUNNING" in status:
        time.sleep(0.1)
    
    data_array = [e.value for _ in execs]

    data_array = np.array(data_array)
    data_array = data_array.transpose().reshape((data_array.shape[1], data_array.shape[2], data_array.shape[0]))

    return data_array

