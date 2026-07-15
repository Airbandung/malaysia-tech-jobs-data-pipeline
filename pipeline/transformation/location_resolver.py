from database.connection import get_db_connection


def resolve_location(cursor, raw_location):
    """
    Resolve raw JobStreet location into structured location data.
    """

    cursor.execute(
        """
        SELECT
            city,
            district,
            locality,
            state,
            country
        FROM location_mapping
        WHERE raw_location = %s
        """,
        (raw_location,)
    )

    result = cursor.fetchone()


    if result:
        return {
            "city": result[0],
            "district": result[1],
            "locality": result[2],
            "state": result[3],
            "country": result[4]
        }


    # fallback if mapping does not exist
    return {
        "city": None,
        "district": None,
        "locality": raw_location,
        "state": None,
        "country": "Malaysia"
    }