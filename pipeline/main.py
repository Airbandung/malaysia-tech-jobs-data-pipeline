from ingestion.sources.kaggle_source import extract_jobstreet_jobs
from ingestion.load_raw_jobs import load_raw_jobs
from pipeline.utils.logger import get_logger
from transformation.transform_jobs import transform_jobs
from analytics.state_summary import generate_state_summary
from pipeline.enrichment.extract_skills import extract_skills

logger = get_logger(__name__)

def main():
    logger.info("Starting ETL...")

    try:
        
        df = extract_jobstreet_jobs()    
        logger.info(f"Extracted {len(df)} job records")
        
        load_raw_jobs(df)
        logger.info("Raw loading complete")

        transform_jobs()
        logger.info("ETL Finished")
        
        extract_skills()
        generate_state_summary()
    
    except Exception as e:
        logger.error(f"Error occurred while extracting jobs: {e}")
        raise

if __name__ == "__main__":
    main()