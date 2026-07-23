from database.connection import get_db_connection
from utils.logger import get_logger


logger = get_logger(__name__)


def get_count(cursor, query):

    cursor.execute(query)

    return cursor.fetchone()[0]


def generate_report():

    conn = get_db_connection()
    cursor = conn.cursor()


    report = {}


    # Raw data
    report["raw_jobs"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM raw_jobs;
        """
    )


    # Transformed jobs
    report["jobs"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM jobs;
        """
    )


    # Companies
    report["companies"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM companies;
        """
    )


    # Locations
    report["locations"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM locations;
        """
    )


    # Skills
    report["skills"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM skills;
        """
    )


    # Jobs with skills
    report["jobs_with_skills"] = get_count(
        cursor,
        """
        SELECT COUNT(DISTINCT job_id)
        FROM job_skills;
        """
    )


    # Roles
    report["roles"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM job_roles;
        """
    )


    # Jobs classified
    report["jobs_with_roles"] = get_count(
        cursor,
        """
        SELECT COUNT(DISTINCT job_id)
        FROM job_role_mapping;
        """
    )


    # Benefits
    report["benefits"] = get_count(
        cursor,
        """
        SELECT COUNT(*)
        FROM benefits;
        """
    )


    # Jobs with benefits
    report["jobs_with_benefits"] = get_count(
        cursor,
        """
        SELECT COUNT(DISTINCT job_id)
        FROM job_benefits;
        """
    )


    cursor.close()
    conn.close()


    return report

if __name__ == "__main__":

    report = generate_report()


    print("\n====== PIPELINE VALIDATION REPORT ======\n")


    for key, value in report.items():

        print(
            f"{key:<25}: {value}"
        )


    print(
        "\n========================================"
    )