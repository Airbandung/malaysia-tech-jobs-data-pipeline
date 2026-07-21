import json
import pandas as pd
import math

from psycopg2.extras import execute_values
from database.connection import get_db_connection
from utils.logger import get_logger

logger = get_logger(__name__)

SOURCE_NAME = "jobstreet_kaggle"

def load_raw_jobs(df: pd.DataFrame):

    conn = get_db_connection()
    cursor = conn.cursor()

    records = []

    for _, row in df.iterrows():
        data = row.to_dict()
        
        #convert NaN values to None
        data = {
            key: (None if (isinstance(value, float) and math.isnan(value)) else value)
            for key, value in data.items()
        }
        
        records.append(
            (
                SOURCE_NAME,
                str(int(row["job_id"])),
                json.dumps(data)
            )
        )

    sql = """
        INSERT INTO raw_jobs
        (
            source,
            external_job_id,
            raw_data
        )
        VALUES %s

        ON CONFLICT (source, external_job_id)
        DO NOTHING;
    """

    execute_values(cursor, sql, records)

    conn.commit()

    logger.info(f"Loaded {len(records)} raw jobs.")

    cursor.close()
    conn.close()