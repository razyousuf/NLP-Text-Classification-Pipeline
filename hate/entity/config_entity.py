from dataclasses import dataclass
from hate.constants import *
import os


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.BUCKET_NAME = BUCKET_NAME # ---> call the BUCKET_NAME from constants
        self.ZIP_FILE_NAME = ZIP_FILE_NAME
        # Paths for data ingestion artifacts
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR) # e.g: Join (hate/artifacts/2025-01-01 12:00:00) with (DataIngestionArtifact) --> hate/artifacts/2025-01-01 12:00:00/DataIngestionArtifact
        self.DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR) # !!! dif.
        self.NEW_DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_RAW_DATA_DIR)
        # Zip file related paths
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, self.ZIP_FILE_NAME)

# Data Validation Config
@dataclass
class DataValidationConfig:
    def __init__(self):
        self.SCHEMA_FILE_PATH: str = CONFIG_DIR
        self.SCHEMA_FILE_NAME: str = SCHEMA_FILE_NAME
        #self.DATA_VALIDATION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_VALIDATION_ARTIFACTS_DIR)
        #self.IMBALANCE_DATA_DIR: str = os.path.join(self.DATA_VALIDATION_ARTIFACTS_DIR, DATA_VALIDATION_IMBALANCE_DATA_DIR)
        #self.RAW_DATA_DIR: str = os.path.join(self.DATA_VALIDATION_ARTIFACTS_DIR, DATA_VALIDATION_RAW_DATA_DIR)
        self.SCHEMA_FILE_PATH: str = os.path.join(self.SCHEMA_FILE_PATH, self.SCHEMA_FILE_NAME)

# Data Transformation Config
@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.DATA_TRANSFORMATION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)
        #self.TRANSFORMED_FILE_NAME: str = TRANSFORMED_FILE_NAME
        self.TRANSFORMED_FILE_PATH: str = os.path.join(self.DATA_TRANSFORMATION_ARTIFACTS_DIR, TRANSFORMED_FILE_NAME)

        self.AXIS: int = AXIS
        self.INPLACE: bool = INPLACE
        self.CLASS: str = CLASS
        self.LABEL: str = LABEL
        self.TWEET: str = TWEET