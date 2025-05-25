# Return values/paths after the execution of the config_entity, as its important for the next component (where the data/file is located?) to get and use these paths.

from dataclasses import dataclass

# Returened constants and their specified data types for data ingestion (for the next component)
@dataclass
class DataIngestionArtifact:
    imbalance_data_file_path: str
    raw_data_file_path: str

# Returned constants and their specified data types for data validation
@dataclass
class DataValidationArtifact:
    imbalance_data_file_path: str
    raw_data_file_path: str
    is_validated: bool

@dataclass
class DataTransformationArtifact:
    transformed_data_path: str


@dataclass
class ModelTrainerArtifacts: 
    trained_model_path:str
    x_test_path: list
    y_test_path: list