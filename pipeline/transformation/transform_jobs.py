import json
from database.connection import get_db_connection
from transformation.location_resolver import resolve_location

def get_pending_jobs():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            raw_job_id,
            external_job_id,
            raw_data
        FROM raw_jobs
        WHERE processing_status = 'pending';
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return jobs

def get_or_create_company(cursor, company_name):

    cursor.execute(
        """
        SELECT company_id
        FROM companies
        WHERE name = %s
        """,
        (company_name,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]


    cursor.execute(
        """
        INSERT INTO companies(name)
        VALUES(%s)
        RETURNING company_id
        """,
        (company_name,)
    )

    company_id = cursor.fetchone()[0]

    return company_id

def get_or_create_location(cursor, location):

    cursor.execute(
        """
        SELECT location_id
        FROM locations
        WHERE
            city IS NOT DISTINCT FROM %s
        AND district IS NOT DISTINCT FROM %s
        AND locality IS NOT DISTINCT FROM %s
        AND state IS NOT DISTINCT FROM %s
        AND country = %s
        """,
        (
            location["city"],
            location["district"],
            location["locality"],
            location["state"],
            location["country"]
        )
    )


    result = cursor.fetchone()

    if result:
        return result[0]


    cursor.execute(
        """
        INSERT INTO locations(
            city,
            district,
            locality,
            state,
            country
        )
        VALUES(%s,%s,%s,%s,%s)
        RETURNING location_id
        """,
        (
            location["city"],
            location["district"],
            location["locality"],
            location["state"],
            location["country"]
        )
    )


    return cursor.fetchone()[0]
    
def insert_job(cursor, raw_job_id, external_job_id, raw_data, company_id, location_id):

    cursor.execute(
        """
        INSERT INTO jobs (
            raw_job_id,
            source,
            external_job_id,
            company_id,
            location_id,
            title,
            description,
            employment_type,
            posted_at,
            metadata
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (source, external_job_id)
        DO NOTHING
        RETURNING job_id
        """,
        (
            raw_job_id,
            "jobstreet_kaggle",
            external_job_id,
            company_id,
            location_id,
            raw_data.get("job_title"),
            raw_data.get("descriptions"),
            raw_data.get("type"),
            raw_data.get("listingDate"),
            json.dumps(raw_data)
        )
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return None

# 5. Mark raw job as completed  <-- ADD HERE
def mark_raw_job_processed(cursor, raw_job_id):

    cursor.execute(
        """
        UPDATE raw_jobs
        SET
            processing_status = 'processed',
            processed_at = CURRENT_TIMESTAMP
        WHERE raw_job_id = %s
        """,
        (raw_job_id,)
    )
    
    
def transform_jobs():

    jobs = get_pending_jobs()

    print(f"Processing {len(jobs)} jobs")

    conn = get_db_connection()
    cursor = conn.cursor()

    for raw_job in jobs:

        raw_job_id = raw_job[0]
        external_job_id = raw_job[1]
        raw_data = raw_job[2]

        company_id = get_or_create_company(
            cursor,
            raw_data["company"]
        )
        
        raw_location = raw_data.get("location")

        if not raw_location or not raw_location.strip():
            continue

        location = resolve_location(
            cursor,
            raw_location
        )

        location_id = get_or_create_location(
            cursor,
            location
        )

        insert_job(
            cursor,
            raw_job_id,
            external_job_id,
            raw_data,
            company_id,
            location_id
        )

        mark_raw_job_processed(
            cursor,
            raw_job_id
        )

    conn.commit()

    cursor.close()
    conn.close()

    print("Transformation complete")
    
if __name__ == "__main__":
    transform_jobs()