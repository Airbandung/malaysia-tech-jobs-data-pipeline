from database.connection import get_db_connection
from utils.logger import get_logger


logger = get_logger(__name__)


def skill_demand():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            s.name,
            COUNT(js.job_id) AS demand

        FROM skills s

        JOIN job_skills js
        ON s.skill_id = js.skill_id

        GROUP BY s.name

        ORDER BY demand DESC

        LIMIT 20;
        """
    )


    results = cursor.fetchall()


    logger.info(
        f"Generated skill demand report: {len(results)} skills"
    )


    for skill, demand in results:
        print(
            f"{skill}: {demand}"
        )


    cursor.close()
    conn.close()



if __name__ == "__main__":
    skill_demand()