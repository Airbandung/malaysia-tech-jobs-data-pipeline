import geopandas as gpd
from database.connection import get_db_connection
from utils.logger import get_logger

logger = get_logger(__name__)

STATE_FILE = "../data/geo/mys_admin_boundaries/mys_admin1.geojson"
DISTRICT_FILE = "../data/geo/mys_admin_boundaries/mys_admin2.geojson"


def update_states(cursor):

    gdf = gpd.read_file(STATE_FILE)

    logger.info(f"Loading {len(gdf)} states")

    for _, row in gdf.iterrows():

        cursor.execute(
            """
            UPDATE malaysia_geo_reference
            SET
                geometry = ST_GeomFromText(%s, 4326),
                latitude = %s,
                longitude = %s
            WHERE
                name = %s
                AND type = 'STATE'
            """,
            (
                row.geometry.wkt,
                row.center_lat,
                row.center_lon,
                row.adm1_name
            )
        )


def insert_districts(cursor):

    gdf = gpd.read_file(DISTRICT_FILE)

    logger.info(f"Loading {len(gdf)} districts")

    for _, row in gdf.iterrows():

        cursor.execute(
            """
            INSERT INTO malaysia_geo_reference(
                name,
                type,
                parent_name,
                state,
                country,
                latitude,
                longitude,
                geometry
            )
            VALUES(
                %s,
                'DISTRICT',
                %s,
                %s,
                'Malaysia',
                %s,
                %s,
                ST_GeomFromText(%s,4326)
            )
            ON CONFLICT DO NOTHING
            """,
            (
                row.adm2_name,
                row.adm1_name,
                row.adm1_name,
                row.center_lat,
                row.center_lon,
                row.geometry.wkt
            )
        )


def main():

    conn = get_db_connection()
    cursor = conn.cursor()

    update_states(cursor)

    insert_districts(cursor)

    conn.commit()

    cursor.close()
    conn.close()

    logger.info("Geo boundaries loaded")


if __name__ == "__main__":
    main()