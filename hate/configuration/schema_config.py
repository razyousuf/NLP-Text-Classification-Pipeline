from hate.logger import logging
from hate.exception import CustomException
import sys

class SchemaConfig:
    def __init__(self, schema: dict):
        self.schema = schema

    def get_dataset_key(self, role: str) -> str:
        """Returns actual dataset key like 'raw_data_set' for role like 'raw_data' """
        try:
            return self.schema["dataset_keys"][role]
        except CustomException as e:
            raise CustomException(e, sys) from e
    def get_drop_columns(self, role: str) -> list[str]:
        try:
            dataset_key = self.get_dataset_key(role)
            return self.schema.get("drop_columns", {}).get(dataset_key, [])
        except CustomException as e:
            raise CustomException(e, sys) from e

    def get_target_column(self, role: str) -> str:
        dataset_key = self.get_dataset_key(role)
        target_list = self.schema.get("targets", {}).get(dataset_key, [])
        if not target_list:
            logging.error(f"No target column defined for dataset role: '{role}'")
        return target_list[0]

    def get_column_groups(self, role: str) -> dict[str, str]:
        try:
            dataset_key = self.get_dataset_key(role)
            return self.schema.get("column_groups", {}).get(dataset_key, {})
        except CustomException as e:
            raise CustomException(e, sys) from e

    def get_all_roles(self) -> list[str]:
        """
        Returns a list of all defined dataset roles (e.g., ['raw', 'imbalance']).
        """
        try:
            return list(self.schema.get("dataset_keys", {}).keys())
        except CustomException as e:
            raise CustomException(e, sys) from e