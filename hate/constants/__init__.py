import os
from datetime import datetime

# Define the base directory for the hate package
TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
BUCKET_NAME = "hate-speach-2025"
ZIP_FILE_NAME = "dataset.zip"
LABEL = "label"
TWEET = "tweet"


# Data Ingestion constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifact"
DATA_INGESTION_IMBALANCE_DATA_DIR = "imbalanced_data.CSV"
DATA_INGESTION_RAW_DATA_DIR = "raw_data.CSV"

