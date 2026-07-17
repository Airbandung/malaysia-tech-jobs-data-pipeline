from database.connection import get_db_connection
from transformation.location_resolver import resolve_location
import re 

def main():

    conn = get_db_connection()
    cursor = conn.cursor()


    test_locations = [
        "Johor Bahru District",
        "Alma, Penang",
        "Pulau Pinang",
        "W.P. Kuala Lumpur",
        "Kuala Lumpur",
        "Sabah",
        "Non Existing Location",
        "Bundusan, Sabah",
        "Shah Alam/Subang",
        "Kuala Nerus District",
        "Manjung District",
        "Bintulu Division",
        "Hulu Langat",
        "Malaysia"
    ]


    for location in test_locations:
        
        
        result = resolve_location(
            cursor,
            location
        )

        print("\nRAW:")
        print(location)

        print("RESULT:")
        print(result)


    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
    