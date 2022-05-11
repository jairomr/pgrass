from pyproj import Transformer
import rasterio
from app.config import logger
from datetime import datetime
from pystac_client import Client
from multiprocessing import Pool, cpu_count
from app.model.point import TimeSerie, Band, Point
from app.db import points, teste
from pydantic import schema_json_of


def read_pixel(name, url, lon, lat, epsg='32721'):
    transformer = Transformer.from_crs("epsg:4326", f"epsg:{epsg}", always_xy=True)
    lon_t, lat_t = transformer.transform(lon, lat)
    with rasterio.open(url) as ds:
        pixel_val = next(ds.sample([(lon_t, lat_t)]))
        return Band(
            name=name,
            value=pixel_val[0],
            url=url)

def to_dict(args):
    item,lon,lat = args
    bands = []
    assets = item.get_assets()
    for asset in assets:
        if assets[asset].roles[0] == 'data':
            bands.append(
                read_pixel(asset, assets[asset].href,lon,lat)
            )
            logger.debug(f'cooder:{(lon,lat)} asset:{asset} url:{assets[asset].href}')
    timeserie = TimeSerie(
        satellite='setinel2',
        datetime=item.datetime,
        bands=bands
    )
    
    logger.info(f'Time {timeserie}')
    return timeserie


async def get_sentinel2(lon,lat,date):
    now = datetime.now()
    catalog_url = "https://earth-search.aws.element84.com/v0"
    catalog = Client.open(catalog_url)

    # Image retrieval parameters
    intersects_dict = dict(type="Point", coordinates=(lon,lat))
    dates =  f'{date}/{now.strftime("%Y-%m-%d")}'

    search = catalog.search(
        collections=["sentinel-s2-l2a-cogs"],
        intersects=intersects_dict,
        datetime=dates
        )
    logger.info(f'Chamando to_dict')
    with Pool(cpu_count()) as works:
        timeseries = works.map(to_dict, [(item,lon,lat) for item in search.get_items()])
    point = Point(
        lat = float(lat),
        lon = float (lon),
        geometry = f"POINT({lon} {lat})",
        timeseries = timeseries
        )
    logger.debug(f'insert: {point.dict()}')
    try:

        result = await points.insert_one(point.dict())
        #t = await teste.insert_one({'teste':'io'})
        #logger.debug(f'insert {t.inserted_id}')
    except Exception as e:
        logger.exception('fall inset in mongodb')
    