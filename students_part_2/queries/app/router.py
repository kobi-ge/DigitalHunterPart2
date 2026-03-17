from fastapi import APIRouter, BackgroundTasks, Response
import logging
import os

from mysql_connection import MysqlConnection
from utils import create_graph, create_two_lists

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



@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@router.get("/movement_quality_targets")
def get_movement_of_quality_targets():
    query = """
        SELECT entity_id, target_name, priority_level 
        FROM targets
        WHERE (priority_level = 1 OR priority_level = 2)
        AND movement_distance_km >= 5;
        """
    result = mysql_instance.get(query=query)
    return result

@router.get("/count_signal_tyoe")
def get_count_signal_type():
    query = """
            SELECT signal_type, COUNT(signal_type) as signal_count
            FROM intel_signals
            GROUP BY signal_type
            ORDER BY  COUNT(signal_type) DESC;
            """
    result = mysql_instance.get(query=query)
    return result

@router.get("/top_3_unknown")
def get_top_3_unknown_entities():
    query = """
        SELECT entity_id, COUNT(entity_id) as reports_amount
        FROM intel_signals
        WHERE priority_level = 99
        GROUP BY entity_id
        order by COUNT(entity_id) DESC
        LIMIT 3;
        """
    result = mysql_instance.get(query=query)
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

