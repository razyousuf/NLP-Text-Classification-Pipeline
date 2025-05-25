import os
from datetime import datetime

# Define the base directory for the hate package
TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
BUCKET_NAME = "hate-speach-2025"
ZIP_FILE_NAME = "dataset.zip"
LABEL = "label"
TWEET = "tweet"

PROJECT_NAME = "hate"

# Data Ingestion constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifact"
DATA_INGESTION_IMBALANCE_DATA_DIR = "imbalanced_data.csv"
DATA_INGESTION_RAW_DATA_DIR = "raw_data.csv"

# Data Validation constants
#CONFIG_DIR = os.path.join("configuration")
#SCHEMA_FILE_NAME = "schema.yaml"
#DATA_VALIDATION_ARTIFACTS_DIR = ARTIFACTS_DIR
#DATA_VALIDATION_IMBALANCE_DATA_DIR = DATA_INGESTION_IMBALANCE_DATA_DIR
#DATA_VALIDATION_RAW_DATA_DIR = DATA_INGESTION_RAW_DATA_DIR
CONFIG_DIR = os.path.join(PROJECT_NAME, "configuration")
SCHEMA_FILE_NAME = "schema.yaml"
#SCHEMA_FILE_PATH = os.path.join(CONFIG_DIR, SCHEMA_FILE_NAME)

# Data Transformation constants
DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformationArtifact"
TRANSFORMED_FILE_NAME = "transformed_data.csv"
DATA_DIR = "data"
AXIS = 1
INPLACE = True
CLASS = "class"