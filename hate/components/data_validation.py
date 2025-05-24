import os
import sys
from hate.logger import logging
from hate.exception import CustomException

import yaml
import pandas as pd

from hate.constants import *
from hate.entity.config_entity import DataValidationConfig
from hate.entity.artifact_entity import DataValidationArtifact
from hate.components.data_ingestion import DataIngestionArtifact


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact

    def read_yaml_schema(self):
        try:
            with open(self.data_validation_config.SCHEMA_FILE_PATH, 'r') as file:
                schema = yaml.safe_load(file)
            return schema
        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_column_names(self, df: pd.DataFrame, expected_columns: list[str]) -> bool:
        return list(df.columns) == expected_columns
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entering the initiate_data_validation method of the DataValidation class.")
        try:
            schema = self.read_yaml_schema()

            imbalance_data_path = self.data_ingestion_artifact.imbalance_data_file_path#, DATA_INGESTION_IMBALANCE_DATA_DIR)
            raw_data_path = self.data_ingestion_artifact.raw_data_file_path

            imbalance_df = pd.read_csv(imbalance_data_path)
            raw_df = pd.read_csv(raw_data_path)

            imbalance_expected_columns = list(schema["imbalance_data_columns"].keys())
            raw_expected_columns = list(schema["raw_data_columns"].keys())
            logging.info(f"Expected columns for imbalance data: {imbalance_expected_columns}")
            logging.info(f"Expected columns for raw data: {raw_expected_columns}")

            is_imbalance_valid = self.validate_column_names(imbalance_df, imbalance_expected_columns)
            is_raw_valid = self.validate_column_names(raw_df, raw_expected_columns)
                
            logging.info(f"Imbalance data column validation result: {is_imbalance_valid}")
            logging.info(f"Raw data column validation result: {is_raw_valid}")
            
            if not (is_imbalance_valid and is_raw_valid):
                logging.error("Data validation failed: Column names do not match expected schema.")

            data_validation_artifact = DataValidationArtifact(
                imbalance_data_file_path=imbalance_data_path,
                raw_data_file_path=raw_data_path,
                is_validated=True
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
