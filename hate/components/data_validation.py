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
from hate.configuration.schema_config import SchemaConfig


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

    def validate_column_names(self, df: pd.DataFrame, expected_schema: dict[str, str], schema_name: str) -> bool:
        expected_columns = list(expected_schema.keys())
        actual_columns = list(df.columns)

        logging.info(f"Expected columns in [{schema_name}]: {expected_columns}")
        logging.info(f"Actual columns in the DataFrame: {actual_columns}")

        return expected_columns == actual_columns


    
    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entering the initiate_data_validation method of the DataValidation class.")
        try:
            # Load schema and wrap with SchemaConfig
            schema = self.read_yaml_schema()
            schema_cfg = SchemaConfig(schema)

            # Automatically resolve paths and roles
            dataset_roles = ["raw_data", "imbalance_data"]
            dataset_paths = {
                "raw_data": self.data_ingestion_artifact.raw_data_file_path,
                "imbalance_data": self.data_ingestion_artifact.imbalance_data_file_path
            }

            # Validate columns for each dataset dynamically
            for role in dataset_roles:
                dataset_key = schema_cfg.get_dataset_key(role)
                df = pd.read_csv(dataset_paths[role])
                expected_columns = schema_cfg.get_column_groups(role)

                if not self.validate_column_names(df, expected_columns, dataset_key):
                    raise ValueError(f"Column validation failed for [{dataset_key}]. Check schema or data format.")

            # All validations passed
            data_validation_artifact = DataValidationArtifact(
                imbalance_data_file_path=dataset_paths["imbalance_data"],
                raw_data_file_path=dataset_paths["raw_data"],
                is_validated=True
            )

            logging.info("Data validation completed successfully.")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
