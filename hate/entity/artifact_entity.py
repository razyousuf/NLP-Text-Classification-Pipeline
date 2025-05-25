# Return values/paths after the execution of the config_entity, as its important for the next component (where the data/file is located?) to get and use these paths.

from dataclasses import dataclass

# Returened constants and their specified data types for data ingestion
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

# Returned constants and their specified data types for data transformation
@dataclass
class DataTransformationArtifact:
    transformed_data_path: str