import re
from database.connection import get_db_connection
SKILLS = [

# Programming
"python",
"java",
"javascript",
"typescript",
"scala",
"go",
"rust",

# Database
"sql",
"mysql",
"postgresql",
"mongodb",
"oracle",

# Data Engineering
"etl",
"elt",
"data pipeline",
"data warehouse",
"data lake",
"spark",
"hadoop",
"kafka",
"airflow",
"dbt",

# Cloud
"aws",
"azure",
"gcp",
"docker",
"kubernetes",
"terraform",

# Data Analysis
"pandas",
"numpy",
"excel",
"tableau",
"power bi",

# ML
"tensorflow",
"pytorch",
"scikit-learn"
]

def extract_skills_from_text(text):

    if not text:
        return []

    text = text.lower()

    found = []

    for skill in SKILLS:

        if re.search(
           r"(?<!\w)" + re.escape(skill) + r"(?!\w) ", 
            text
        ):
            found.append(skill)

    return found

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
    
    
def process_skills():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT job_id, description
        FROM jobs
        """
    )


    jobs = cursor.fetchall()

    print(f"Processing skills for {len(jobs)} jobs")


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


    conn.commit()

    cursor.close()
    conn.close()


    print("Skill extraction complete")
    
if __name__ == "__main__":

    process_skills()