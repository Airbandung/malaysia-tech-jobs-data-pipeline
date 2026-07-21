from database.connection import get_db_connection
from enrichment.role_classifier import ROLE_RULES
from utils.logger import get_logger

logger = get_logger(__name__)

def classify_role(title, description):

    title_text = title.lower() if title else ""

    description_text = description.lower() if description else ""


    # 1. Check title first
    for role, keywords in ROLE_RULES.items():

        for keyword in keywords:

            if keyword in title_text:
                return role, 1.0


   # Second pass: description fallback
    for role, keywords in ROLE_RULES.items():

        for keyword in keywords:

            if keyword in description_text:
                return role, 0.5


    return None, 0.0



def get_or_create_role(cursor, role):

    cursor.execute(
        """
        INSERT INTO job_roles(name)

        VALUES(%s)

        ON CONFLICT(name)
        DO UPDATE SET name = EXCLUDED.name

        RETURNING role_id
        """,
        (role,)
    )

    return cursor.fetchone()[0]



def insert_job_role(cursor, job_id, role_id, confidence):

    cursor.execute(
        """
        INSERT INTO job_role_mapping
        (
            job_id,
            role_id,
            confidence
        )

        VALUES(%s,%s,%s)

        ON CONFLICT(job_id)
        DO UPDATE SET

        role_id = EXCLUDED.role_id,
        confidence = EXCLUDED.confidence
        """,
        (
            job_id,
            role_id,
            confidence
        )
    )



def classify_jobs():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            job_id,
            title,
            description

        FROM jobs
        """
    )


    jobs = cursor.fetchall()

    logger.info(f"Processing {len(jobs)} jobs")


    classified = 0


    for job_id, title, description in jobs:


        role, confidence = classify_role(
            title,
            description
        )


        if role:

            role_id = get_or_create_role(
                cursor,
                role
            )


            insert_job_role(
                cursor,
                job_id,
                role_id,
                confidence
            )
            classified += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Classified {classified} jobs")


if __name__ == "__main__":
    classify_jobs()