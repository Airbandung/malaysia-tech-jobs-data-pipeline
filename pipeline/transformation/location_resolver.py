import re
STATE_ALIASES = {
    "kuala lumpur": "W.P. Kuala Lumpur",
    "penang": "Pulau Pinang",
}

def resolve_location(cursor, raw_location):
    
    clean_location = re.sub(
        r"\s+District$",
        "",
        raw_location,
        flags=re.IGNORECASE
    )
    
    
    result = {
        "city": None,
        "district": None,
        "locality": raw_location,
        "state": None,
        "country": "Malaysia",
        "geo_id": None
    }
    
    if clean_location.lower() == "malaysia":
        result["country"] = "Malaysia"
        return result



    # 1. Exact match against geo reference

    cursor.execute(
        """
        SELECT
            geo_id,
            name,
            type,
            parent_name,
            state
        FROM malaysia_geo_reference
        WHERE LOWER(name)=LOWER(%s)
        OR LOWER(name)=LOWER(
            regexp_replace(%s, '\\s+(District|Division)$', '', 'i')
        )
        """,
        (
            clean_location,
            clean_location
        )
    )


    row = cursor.fetchone()


    if row:

        geo_id, name, geo_type, parent, state = row

        result["geo_id"] = geo_id


        if geo_type == "STATE":

            result["state"] = name


        elif geo_type == "DISTRICT":

            result["district"] = name
            result["state"] = state


        return result

    # State aliases
    alias = STATE_ALIASES.get(
        clean_location.lower()
    )

    if alias:

        cursor.execute(
            """
            SELECT
                geo_id,
                name
            FROM malaysia_geo_reference
            WHERE name = %s
            AND type = 'STATE'
            """,
            (alias,)
        )

        row = cursor.fetchone()

        if row:

            result["geo_id"] = row[0]
            result["state"] = row[1]

            return result

    # 2. Check comma format
    # Example:
    # Alma, Penang

    if "," in clean_location:

        parts = [
            x.strip()
            for x in clean_location.split(",")
        ]


        place = parts[0]
        possible_state = parts[-1]
        
        possible_state = STATE_ALIASES.get(
            possible_state.lower(),
            possible_state
        )


        cursor.execute(
            """
            SELECT
                geo_id,
                name,
                type,
                state
            FROM malaysia_geo_reference
            WHERE LOWER(name)=LOWER(%s)
            AND LOWER(state)=LOWER(%s)
            """,
            (
                place,
                possible_state
            )
        )


        row = cursor.fetchone()


        if row:

            geo_id,name,geo_type,state=row

            result["geo_id"] = geo_id
            if geo_type == "DISTRICT":
                result["district"] = name
            elif geo_type == "STATE":
                result["state"] = name
            else:
                result["city"] = name

            return result

        result["city"] = place
        result["state"] = possible_state

        return result



    # 3. Alias lookup

    cursor.execute(
        """
        SELECT
            l.geo_id,
            g.name,
            g.type,
            g.state
        FROM location_aliases l
        JOIN malaysia_geo_reference g
        ON l.geo_id = g.geo_id
        WHERE LOWER(l.alias_name)=LOWER(%s)
        """,
        (clean_location,)
    )

    row = cursor.fetchone()


    if row:

        geo_id, name, geo_type, state = row

        result["geo_id"] = geo_id
        result["state"] = state

        if geo_type == "DISTRICT":
            result["district"] = name

        return result



    # 4. Unknown

    result["locality"] = raw_location

    return result
