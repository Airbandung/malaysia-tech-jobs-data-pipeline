from database.connection import get_db_connection
from transformation.location_resolver import resolve_location
from utils.logger import get_logger

logger = get_logger(__name__)

def build_location_mapping():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT DISTINCT
            raw_data->>'location'
        FROM raw_jobs
    """)


    locations = cursor.fetchall()


    logger.info(f"Found {len(locations)} locations")


    for row in locations:

        raw_location = row[0]


        result = resolve_location(
            cursor,
            raw_location
        )


        cursor.execute(
            """
            INSERT INTO location_mapping
            (
                raw_location,
                city,
                district,
                locality,
                state,
                country,
                geo_id
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s
            )

            ON CONFLICT(raw_location)
            DO UPDATE SET

                city = EXCLUDED.city,
                district = EXCLUDED.district,
                locality = EXCLUDED.locality,
                state = EXCLUDED.state,
                geo_id = EXCLUDED.geo_id

            """,
            (
                raw_location,
                result["city"],
                result["district"],
                result["locality"],
                result["state"],
                result["country"],
                result["geo_id"]
            )
        )


    conn.commit()

    cursor.close()
    conn.close()


    logger.info("Location mapping generated")


if __name__ == "__main__":
    build_location_mapping()