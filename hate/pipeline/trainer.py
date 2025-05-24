import sys
from hate.logger import logging
from hate.exception import CustomException
from hate.components.data_ingestion import DataIngestion

from hate.entity.config_entity import (DataIngestionConfig)

from hate.entity.artifact_entity import (DataIngestionArtifact)


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Starting the data ingestion training pipeline...")
        try:
            logging.info("Getting data from GCloud storage...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train and validation data from GCloud storage.")
            logging.info("Exiting the start_data_ingestion method of the TrainingPipeline class..")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of the TrainingPipeline class..")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info("Exited the run_pipeline method of the TrainingPipeline class..")
        except Exception as e:
            raise CustomException(e, sys) from e