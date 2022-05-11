from fastapi import APIRouter

from datetime import datetime
from pystac_client import Client
from ...fuctions.sentinel2 import to_dict
from ...config import logger
from multiprocessing import Pool, cpu_count


router = APIRouter()

@router.get('/')
def get_sentinel2():
    now = datetime.now()
    catalog_url = "https://earth-search.aws.element84.com/v0"
    catalog = Client.open(catalog_url)

    # Image retrieval parameters
    intersects_dict = dict(type="Point", coordinates=(-55,-14))
    dates =  f'2015-06-01/{now.strftime("%Y-%m-%d")}'

    search = catalog.search(
        collections=["sentinel-s2-l2a-cogs"],
        intersects=intersects_dict,
        datetime=dates
        )
    logger.info(f'Chamando to_dict')
    with Pool(cpu_count()*8) as works:
        result = works.map(to_dict, [(item,-55,-14) for item in search.get_items()])

    return result


