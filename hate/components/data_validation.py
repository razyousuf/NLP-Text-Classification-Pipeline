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

    def validate_column_names(self, df: pd.DataFrame, schema_columns: dict[str, str], schema_name: str) -> bool:
        expected_columns = list(schema_columns.keys())
        actual_columns = list(df.columns)

        logging.info(f"Expected columns in [{schema_name}] are: {expected_columns}")
        logging.info(f"Actual columns in the DataFrame are: {actual_columns}")

        return expected_columns == actual_columns

    
    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entering the initiate_data_validation method of the DataValidation class.")
        try:
            schema = self.read_yaml_schema()
            column_types = schema["column_types"]

            imbalance_data_path = self.data_ingestion_artifact.imbalance_data_file_path
            raw_data_path = self.data_ingestion_artifact.raw_data_file_path
            # Load both datasets as tuples of (DataFrame, schema_key)
            datasets = [
                (pd.read_csv(imbalance_data_path), "imbalance_data"),
                (pd.read_csv(raw_data_path), "raw_data")
            ]

            for df, name in datasets:
                if not self.validate_column_names(df, column_types[name], name):
                    logging.error(f"Column validation failed for [{name}]. Please check the schema.")


            data_validation_artifact = DataValidationArtifact(
                imbalance_data_file_path=imbalance_data_path,
                raw_data_file_path=raw_data_path,
                is_validated=True
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
