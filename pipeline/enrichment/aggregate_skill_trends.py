from database.connection import get_db_connection
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_skill_trends():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO skill_trends
        (
            skill_id,
            month,
            demand_count
        )

        SELECT
            js.skill_id,

            DATE_TRUNC(
                'month',
                j.posted_at
            )::date AS month,

            COUNT(*) AS demand_count


        FROM job_skills js

        JOIN jobs j
        ON js.job_id = j.job_id


        WHERE j.posted_at IS NOT NULL


        GROUP BY
            js.skill_id,
            DATE_TRUNC(
                'month',
                j.posted_at
            )


        ON CONFLICT(skill_id, month)

        DO UPDATE SET

            demand_count =
            EXCLUDED.demand_count
        """
    )


    conn.commit()

    cursor.close()
    conn.close()


    logger.info("Skill trends generated")


if __name__ == "__main__":
    generate_skill_trends()