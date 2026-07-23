import re 

from database.connection import get_db_connection
from utils.logger import get_logger
from enrichment.constant import BENEFIT_MAPPING
from enrichment.constant import BENEFIT_HEADERS

logger = get_logger(__name__)

BENEFIT_HEADERS = sorted(
    BENEFIT_HEADERS,
    key=len,
    reverse=True
)


def extract_benefit_section(description):

    if not description:
        return ""

    text = description.lower()

    start = None

    for header in BENEFIT_HEADERS:

        idx = text.find(header)

        if idx != -1:
            start = idx
            break

    if start is None:
        return ""

    section = text[start:]

    return section

def extract_benefits_from_text(section):

    found = set()

    for benefit, info in BENEFIT_MAPPING.items():

        for keyword in info["keywords"]:

            if keyword in section:

                found.add(benefit)
                break

    return list(found)

def get_or_create_benefit(cursor, name):

    category = BENEFIT_MAPPING[name]["category"]

    cursor.execute(
        """
        INSERT INTO benefits(
            name,
            category
        )
        VALUES(%s,%s)

        ON CONFLICT(name)
        DO UPDATE SET
            category = EXCLUDED.category

        RETURNING benefit_id
        """,
        (
            name,
            category
        )
    )

    return cursor.fetchone()[0]


def insert_job_benefit(
    cursor,
    job_id,
    benefit_id
):

    cursor.execute(
        """
        INSERT INTO job_benefits(
            job_id,
            benefit_id
        )

        VALUES(%s,%s)

        ON CONFLICT(job_id, benefit_id)
        DO NOTHING
        """,
        (
            job_id,
            benefit_id
        )
    )

def extract_benefits():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            job_id,
            description

        FROM jobs
        """
    )


    jobs = cursor.fetchall()

    logger.info(
        f"Processing {len(jobs)} jobs"
    )


    processed = 0


    for job_id, description in jobs:


        section = extract_benefit_section(
            description
        )


        benefits = extract_benefits_from_text(
            section
        )


        for benefit in benefits:


            benefit_id = get_or_create_benefit(
                cursor,
                benefit
            )


            insert_job_benefit(
                cursor,
                job_id,
                benefit_id
            )


        processed += 1


        if processed % 5000 == 0:
            logger.info(
                f"Processed {processed} jobs"
            )


    conn.commit()

    cursor.close()
    conn.close()


    logger.info(
        "Benefit extraction complete"
    )


if __name__ == "__main__":

    extract_benefits()