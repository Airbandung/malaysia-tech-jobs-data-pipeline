from transformation.malaysia_location import KNOWN_LOCATIONS
MALAYSIA_STATES = [
    "Johor",
    "Kedah",
    "Kelantan",
    "Melaka",
    "Negeri Sembilan",
    "Pahang",
    "Penang",
    "Perak",
    "Perlis",
    "Sabah",
    "Sarawak",
    "Selangor",
    "Terengganu",
    "Kuala Lumpur",
    "Putrajaya",
    "Labuan"
]


def normalize_location(raw_location):

    location = raw_location.strip()


    # check known mapping first

    if location in KNOWN_LOCATIONS:
        return (
            location,
            KNOWN_LOCATIONS[location]
        )


    # existing comma logic

    if "," in location:

        parts = [
            x.strip()
            for x in location.split(",")
        ]

        city = parts[0]
        state = parts[-1]

        if state in MALAYSIA_STATES:
            return city,state


    return location, None