import os
import sys
from hate.logger import logging
from hate.exception import CustomException

import pandas as pd
import yaml
import string 
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
#from sklearn.model_selection import train_test_split

from hate.constants import *
from hate.entity.config_entity import DataTransformationConfig, DataValidationConfig
from hate.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact
from hate.components.data_validation import DataValidationArtifact
from hate.configuration.schema_config import SchemaConfig

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact
        self.data_validation_config = DataValidationConfig()
        
        self.stemmer = nltk.SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))

    def read_yaml_schema(self):
        try:
            with open(self.data_validation_config.SCHEMA_FILE_PATH, 'r') as file:
                schema = yaml.safe_load(file)
            return schema
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def imbalance_data_cleaning(self):
        try:
            logging.info("Entering the imbalance_data_cleaning method of the DataTransformation class.")

            # Load YAML schema and use SchemaConfig abstraction
            schema = self.read_yaml_schema()
            schema_cfg = SchemaConfig(schema)

            # Dynamically resolve dataset role and paths
            #cleaned_key = schema_cfg.get_dataset_key("imbalance_data")
            drop_cols = schema_cfg.get_drop_columns("imbalance_data")
            
            # Load the imbalance data using dynamic key
            imbalance_data_path = self.data_validation_artifact.imbalance_data_file_path
            imbalance_data = pd.read_csv(imbalance_data_path)

            # Clean the data
            imbalance_data.dropna(inplace=True)
            imbalance_data.drop(
                columns=drop_cols,
                axis=self.data_transformation_config.AXIS,
                inplace=self.data_transformation_config.INPLACE
            )
            
            logging.info("Exiting the imbalance_data_cleaning method successfully.")
            return imbalance_data

        except Exception as e:
            raise CustomException(e, sys) from e

        
    def raw_data_cleaning(self):
        try:
            logging.info("Entering the raw_data_cleaning method of the DataTransformation class.")
            schema = self.read_yaml_schema()
            schema_cfg = SchemaConfig(schema)

            #raw_key = schema_cfg.get_dataset_key("raw_data")
            #cleaned_key = schema_cfg.get_dataset_key("imbalance_data")

            target_col_raw = schema_cfg.get_target_column("raw_data")
            target_col_imbalance = schema_cfg.get_target_column("imbalance_data")
            drop_cols = schema_cfg.get_drop_columns("raw_data")

            raw_data_path = self.data_validation_artifact.raw_data_file_path
            raw_data = pd.read_csv(raw_data_path)

            raw_data.dropna(inplace=True)
            raw_data.drop(columns=drop_cols, axis=self.data_transformation_config.AXIS, inplace=True)
            # Add class 1 to class 0
            raw_data[raw_data[target_col_raw] == 0] [target_col_raw] = 1
            # Replace the value 0  → 1
            raw_data[target_col_raw].replace({0:1}, inplace=True)
            # Replace class 2 → 0
            raw_data[target_col_raw].replace({2: 0}, inplace=True)
    
            raw_data.rename(columns={target_col_raw: target_col_imbalance}, inplace=True)

            logging.info("Cleaned and returned raw_data")
            return raw_data
        
        except Exception as e:
            raise CustomException(e, sys) from e

    def concat_dataframe(self):
        try:
            logging.info("Entering the concat_data method of the DataTransformation class.")
            frame = [self.imbalance_data_cleaning(), self.raw_data_cleaning()]
            df = pd.concat(frame)
            print(df.head())
            logging.info("Exiting the concat_data method and returned the concatenated data.")
            return df
        except Exception as e:
            raise CustomException(e, sys) from e

    def concat_data_cleaning(self, text):
        """
        Cleans input text by removing noise such as punctuation, HTML tags, emojis,
        URLs, stopwords, and performs stemming.
        """
        try:
            # Convert to lowercase and ensure it's a string
            text = str(text).lower()

            # Remove URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text)

            # Remove HTML tags
            text = re.sub(r'<.*?>', '', text)

            # Remove text in square brackets
            text = re.sub(r'\[.*?\]', '', text)

            # Remove emojis and non-ASCII characters
            text = text.encode('ascii', 'ignore').decode('ascii')

            # Remove punctuation
            text = re.sub(rf"[{re.escape(string.punctuation)}]", '', text)

            # Remove words with numbers (e.g. "covid19")
            text = re.sub(r'\w*\d\w*', '', text)

            # Remove newlines and extra spaces
            text = re.sub(r'\s+', ' ', text).strip()

            # Tokenize and remove stopwords
            tokens = [word for word in text.split() if word not in self.stop_words]

            # Apply stemming
            stemmed_tokens = [self.stemmer.stem(word) for word in tokens]

            return ' '.join(stemmed_tokens)

        except Exception as e:
            raise CustomException(e, sys) from e

        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Entering the initiate_data_transformation method of the DataTransformation class.")
            
            self.imbalance_data_cleaning()
            self.raw_data_cleaning()
            df = self.concat_dataframe()
            df[self.data_transformation_config.TWEET] = df[self.data_transformation_config.TWEET].apply(self.concat_data_cleaning)
            
            logging.info(f"transformed data: {df.head()}, shape: {df.shape}")
            
            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR, exist_ok=True)
            df.to_csv(self.data_transformation_config.TRANSFORMED_FILE_PATH, index=False, header=True)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_data_path = self.data_transformation_config.TRANSFORMED_FILE_PATH
            )
            logging.info("Exiting the initiate_data_transformation method and returned the data transformation artifact {data_transformation_artifact}.")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e