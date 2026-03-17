from fastapi import APIRouter, BackgroundTasks, Response
import logging
import os

from mysql_connection import MysqlConnection
from utils import create_graph, create_two_lists
from dal import *

router = APIRouter()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(MysqlConnection.__module__)


mysql_instance = MysqlConnection(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=os.getenv("MYSQL_PORT", 3306),
    password=os.getenv("MYSQL_PASSWORD", "root"),
    user=os.getenv("MYSQL_USER", "root"),
    database=os.getenv("MYSQL_DATABASE", "digital_hunter"),
    logger=logger
)
mysql_instance.connect()



@router.get("/movement_quality_targets")
def get_movement_of_quality_targets():
    result = mysql_instance.get(query=get_movement_of_quality_targets_query)
    return result

@router.get("/count_signal_type")
def get_count_signal_type():
    result = mysql_instance.get(query=get_count_signal_type_query)
    return result

@router.get("/top_3_unknown")
def get_top_3_unknown_entities():
    result = mysql_instance.get(query=get_top_3_unknown_entities_query)
    return result

@router.get("/targets_wake_up")
def get_targets_that_wakes_up():
    result = mysql_instance.get(query=get_targets_that_wakes_up_query)
    return result
    

@router.get("/entity_id_graph")
def create_entity_id_graph(background_tasks: BackgroundTasks, entity_id: str):
    query = f"""
        SELECT reported_lon, reported_lat
        FROM intel_signals 
        WHERE entity_id LIKE '{entity_id}';
        """
    result = mysql_instance.get(query=query)
    xpoints, ypoints = create_two_lists(result)
    img_buf = create_graph(
    xpoints=xpoints,
    ypoints=ypoints
    )
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')

