from database.connection import get_db_connection
from enrichment.skill_extractor import extract_skills_from_text


def get_or_create_skill(cursor, skill):

    cursor.execute(
        """
        INSERT INTO skills(name)
        VALUES(%s)

        ON CONFLICT(name)
        DO UPDATE SET name = EXCLUDED.name

        RETURNING skill_id
        """,
        (skill,)
    )

    return cursor.fetchone()[0]


def insert_job_skill(cursor, job_id, skill_id):

    cursor.execute(
        """
        INSERT INTO job_skills(
            job_id,
            skill_id,
            skill_type
        )
        VALUES(%s,%s,%s)

        ON CONFLICT(job_id, skill_id)
        DO NOTHING
        """,
        (
            job_id,
            skill_id,
            "technical"
        )
    )


def extract_skills():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT job_id, description
        FROM jobs
        """
    )


    jobs = cursor.fetchall()

    print(
        f"Processing {len(jobs)} jobs"
    )


    count = 0

    for job_id, description in jobs:

        skills = extract_skills_from_text(
            description
        )


        for skill in skills:

            skill_id = get_or_create_skill(
                cursor,
                skill
            )

            insert_job_skill(
                cursor,
                job_id,
                skill_id
            )


        count += 1

        if count % 1000 == 0:
            conn.commit()
            print(
                f"{count} jobs processed"
            )


    conn.commit()

    cursor.close()
    conn.close()

    print("Skill extraction complete")


if __name__ == "__main__":
    extract_skills()