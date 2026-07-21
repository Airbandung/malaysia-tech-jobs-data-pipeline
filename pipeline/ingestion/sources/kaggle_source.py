import os
import pandas as pd
import kagglehub
from utils.logger import get_logger

logger = get_logger(__name__)

DATASET = "azraimohamad/jobstreet-all-job-dataset"


def extract_jobstreet_jobs():

    dataset_path = kagglehub.dataset_download(DATASET)

    csv_file = None

    for file in os.listdir(dataset_path):
        if file.endswith(".csv"):
            csv_file = os.path.join(dataset_path, file)
            break

    if csv_file is None:
        logger.error("No CSV file found in dataset")
        raise FileNotFoundError("No CSV file found in dataset")

    df = pd.read_csv(csv_file)
    logger.info(f"Extracted {len(df)} job records")

    return df