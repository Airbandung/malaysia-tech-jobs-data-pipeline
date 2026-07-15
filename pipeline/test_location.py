from database.connection import get_db_connection
from transformation.location_resolver import resolve_location


def main():

    conn = get_db_connection()
    cursor = conn.cursor()

    test_locations = [
        "Alma, Penang",
        "Bundusan, Sabah",
        "Shah Alam/Subang",
        "Kuala Lumpur",
        "Non Existing Location"
    ]

    for location in test_locations:

        result = resolve_location(
            cursor,
            location
        )

        print("\nRAW:")
        print(location)

        print("RESOLVED:")
        print(result)


    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()