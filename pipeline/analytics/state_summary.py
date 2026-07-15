from database.connection import get_db_connection

def generate_state_summary():

    conn = get_db_connection()
    cursor = conn.cursor()

    print("Generating state summary...")

    # Remove previous summary
    cursor.execute("DELETE FROM state_job_summary")

    # Aggregate jobs by state
    cursor.execute("""
        INSERT INTO state_job_summary (state, total_jobs)
        SELECT
            l.state,
            COUNT(*)
        FROM jobs j
        JOIN locations l
            ON j.location_id = l.location_id
        GROUP BY l.state
        ORDER BY COUNT(*) DESC;
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("State summary complete.")
    
if __name__ == "__main__":
    generate_state_summary()