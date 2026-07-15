from database.connection import get_db_connection
from transformation.location_normalizer import normalize_location


def build_location_mapping():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT DISTINCT
            raw_data->>'location'
        FROM raw_jobs
    """)

    locations = cursor.fetchall()


    print(f"Found {len(locations)} locations")


    for row in locations:

        raw_location = row[0]

        city, state = normalize_location(
            raw_location
        )


        cursor.execute(
            """
            INSERT INTO location_mapping
            (
                raw_location,
                city,
                state
            )
            VALUES
            (
                %s,
                %s,
                %s
            )

            ON CONFLICT(raw_location)
            DO NOTHING
            """,
            (
                raw_location,
                city,
                state
            )
        )


    conn.commit()

    cursor.close()
    conn.close()


    print("Location mapping generated")


if __name__ == "__main__":
    build_location_mapping()