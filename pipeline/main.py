from ingestion.sources.kaggle_source import extract_jobstreet_jobs
from ingestion.load_raw_jobs import load_raw_jobs
from transformation.transform_jobs import transform_jobs

def main():

    print("Starting ETL...")

    df = extract_jobstreet_jobs()

    print(f"Extracted {len(df)} job records")

    load_raw_jobs(df)

    print("Raw loading complete")

    transform_jobs()

    print("ETL Finished")

if __name__ == "__main__":
    main()