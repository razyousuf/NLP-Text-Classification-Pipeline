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

# Model Training constants
MODEL_TRAINER_ARTIFACTS_DIR = "ModelTrainerArtifacts"
TRAINED_MODEL_DIR = "trained_model"
TRAINED_MODEL_NAME = "model.h5"
X_TEST_FILE_NAME = "X_test.csv"
Y_TEST_FILE_NAME = "Y_test.csv"
X_TRAIN_FILE_NAME = "X_train.csv"

RANDOM_STATE = 42
EPOCHS = 1
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.2

# Model Architecture constants
MAX_WORDS = 50000
MAX_LEN = 300
LOSS = "binary_crossentropy"
METRICS = ["accuracy"]
ACTIVATION = "sigmoid"

# Model Evaluation constants
MODEL_EVALUATION_ARTIFACTS_DIR = "ModelEvaluationArtifacts"
BEST_MODEL_DIR = "best_model"
MODEL_EVALUATION_FILE_NAME = "loss.csv"

MODEL_NAME = "model.h5"
APP_HOST = "0.0.0.0"
APP_PORT = 8080


# Model Pusher constants
    # No need any new constants, as we now have them all