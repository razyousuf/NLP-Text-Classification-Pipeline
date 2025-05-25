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

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact
        self.data_validation_config = DataValidationConfig()

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
            imbalance_data_path = self.data_validation_artifact.imbalance_data_file_path
            imbalance_data = pd.read_csv(imbalance_data_path)

            imbalance_data.dropna(inplace=True)
            drop_cols = self.read_yaml_schema()["drop_columns"]["imbalance_data"]
            imbalance_data.drop(
                columns=drop_cols, 
                axis=self.data_transformation_config.AXIS, 
                inplace=self.data_transformation_config.INPLACE
                )
            
            logging.info("Exiting the imbalance_data_cleaning method and returned the imbalance data {imbalance_data}.")
            return imbalance_data

        except Exception as e:
            raise CustomException(e, sys) from e
        
    def raw_data_cleaning(self):
        try:
            logging.info("Entering the raw_data_cleaning method of the DataTransformation class.")
             # Load file
            raw_data_path = self.data_validation_artifact.raw_data_file_path
            raw_data = pd.read_csv(raw_data_path)
            raw_data.dropna(inplace=True)

            # Read schema
            schema = self.read_yaml_schema()
            drop_columns = schema["drop_columns"]["raw_data"]
            target_column = schema["targets"]["raw_data"][0]  # dynamically use the column named "class"
            new_label_column = schema["targets"]["imbalance_data"][0]  # this is what you're renaming to ("label")

            # Drop irrelevant columns
            raw_data.drop(
                columns=drop_columns,
                axis=self.data_transformation_config.AXIS,
                inplace=self.data_transformation_config.INPLACE
            )
            # Clean and relabel target
            raw_data.loc[raw_data[target_column] == 1, target_column] = 1
            raw_data.loc[raw_data[target_column] == 0, target_column] = 1
            raw_data[target_column].replace({2: 0}, inplace=True)

            # Rename column (e.g., "class" → "label")
            raw_data.rename(columns={target_column: new_label_column}, inplace=True)

            logging.info(f"Exiting the raw_data_cleaning method and returned the cleaned raw_data.")
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

    def concat_data_cleaning(self, words):
        try:
            logging.info("Entering the concat_data_cleaning method of the DataTransformation class.")
            # Apply stemmer and stopwords removal on the data
            stemmer = nltk.SnowballStemmer('english')
            stop_words = set(stopwords.words('english'))
            words = str(words).lower()
            words = re.sub('\[.*?\]', '', words)  # Remove text in square brackets
            words = re.sub('[%s]' % re.escape(string.punctuation), '', words)  # Remove punctuation
            words = re.sub('\w*\d\w*', '', words)  # Remove words containing numbers
            words = re.sub('http\S+|www\S+|https\S+', '', words, flags=re.MULTILINE)  # Remove URLs
            words = re.sub('<.*?>+', '', words)  # Remove HTML tags
            words = re.sub('\n', '', words)  # Remove new lines
            words = re.sub('\s+', ' ', words).strip()  # Remove extra spaces
            words = [word for word in words.split(' ') if word not in stop_words] # Remove stopwords
            words = " ".join(words) # Join the words back into a single string
            words = [stemmer.stem(words) for words in words.split(' ')]  # Apply stemming
            words = " ".join(words)  
            logging.info("Exiting the concat_data_cleaning method and returned the cleaned data.")
            return words


        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Entering the initiate_data_transformation method of the DataTransformation class.")
            
            self.imbalance_data_cleaning()
            self.raw_data_cleaning()
            df = self.concat_dataframe()
            df[self.data_transformation_config.TWEET] = df[self.data_transformation_config.TWEET].apply(self.concat_data_cleaning)

            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR, exist_ok=True)
            df.to_csv(self.data_transformation_config.TRANSFORMED_FILE_PATH, index=False, header=True)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_data_path = self.data_transformation_config.TRANSFORMED_FILE_PATH
            )
            logging.info("Exiting the initiate_data_transformation method and returned the data transformation artifact {data_transformation_artifact}.")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e