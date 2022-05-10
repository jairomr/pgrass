from pyproj import Transformer
import rasterio
from ..config import logger

def read_pixel(url, lon, lat, epsg='32721'):
    transformer = Transformer.from_crs("epsg:4326", f"epsg:{epsg}", always_xy=True)
    lon_t, lat_t = transformer.transform(lon, lat)
    with rasterio.open(url) as ds:
        pixel_val = next(ds.sample([(lon_t, lat_t)]))
        return (str(pixel_val[0]),url)

def to_dict(args):
    item,lon,lat = args
    bands = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B11', 'B12', 'AOT', 'WVP', 'SCL']
    result = {}
    assets = item.get_assets()
    
    for name in bands:
        logger.info(f"url:{assets[name].href}, x: {lon} y: {lat}")
        result[name] = read_pixel(assets[name].href,lon,lat)
    
    return {
        'name':item.id, 
        'datetime':str(item.datetime),
        'geometry':f"POINT({lon} {lat})",
        'bands':result}
