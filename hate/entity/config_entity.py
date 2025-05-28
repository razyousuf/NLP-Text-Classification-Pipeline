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


# Model Trainer Config
@dataclass
class ModelTrainerConfig: 
    def __init__(self):
        self.TRAINED_MODEL_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,MODEL_TRAINER_ARTIFACTS_DIR) 
        self.TRAINED_MODEL_PATH = os.path.join(self.TRAINED_MODEL_DIR,TRAINED_MODEL_NAME)
        self.X_TEST_DATA_PATH = os.path.join(self.TRAINED_MODEL_DIR, X_TEST_FILE_NAME)
        self.Y_TEST_DATA_PATH = os.path.join(self.TRAINED_MODEL_DIR, Y_TEST_FILE_NAME)
        self.X_TRAIN_DATA_PATH = os.path.join(self.TRAINED_MODEL_DIR, X_TRAIN_FILE_NAME)
        self.MAX_WORDS = MAX_WORDS
        self.MAX_LEN = MAX_LEN
        self.LOSS = LOSS
        self.METRICS = METRICS
        self.ACTIVATION = ACTIVATION
        self.LABEL = LABEL
        self.TWEET = TWEET
        self.RANDOM_STATE = RANDOM_STATE
        self.EPOCH = EPOCHS
        self.BATCH_SIZE = BATCH_SIZE
        self.VALIDATION_SPLIT = VALIDATION_SPLIT


# Model Evaluation Config
@dataclass
class ModelEvaluationConfig:
    def __init__(self):
        self.MODEL_EVALUATION_MODEL_DIR: str = os.path.join(os.getcwd(), ARTIFACTS_DIR, MODEL_EVALUATION_ARTIFACTS_DIR)
        self.BEST_MODEL_DIR_PATH: str = os.path.join(self.MODEL_EVALUATION_MODEL_DIR, BEST_MODEL_DIR)
        self.BUCKET_NAME = BUCKET_NAME
        self.MODEL_NAME = MODEL_NAME
        #self.THRESHOLD_FILE_NAME = THRESHOLD_FILE_NAME
        self.EVALUATION_METRICS_FILE = EVALUATION_METRICS_FILE


# Model Pusher Config
@dataclass
class ModelPusherConfig:
    def __init__(self):
        self.TRAINED_MODEL_PATH: str = os.path.join(os.getcwd(), ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR)
        self.BUCKET_NAME = BUCKET_NAME
        self.MODEL_NAME = MODEL_NAME