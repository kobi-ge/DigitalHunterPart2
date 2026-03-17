from fastapi import APIRouter
from mysql_connection import MysqlConnection
import logging

router = APIRouter()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

query = """
SELECT * FROM targets;
"""
mysql_instance = MysqlConnection(
    host="localhost",
    port=3306,
    password="root",
    user="root",
    database="digital_hunter",
    logger=logging.getLogger("asdf")
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