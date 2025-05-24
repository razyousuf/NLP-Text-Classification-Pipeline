import sys
from hate.logger import logging
from hate.exception import CustomException
from hate.components.data_ingestion import DataIngestion
from hate.components.data_validation import DataValidation

from hate.entity.config_entity import (DataIngestionConfig,
                                       DataValidationConfig
                                       )


from hate.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact
                                        )


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()


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
        

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Starting the data validation training pipeline...")
        try:

            data_validation = DataValidation(data_validation_config=self.data_validation_config, data_ingestion_artifact=data_ingestion_artifact)

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully.")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e



    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of the TrainingPipeline class..")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info("Exited the run_pipeline method of the TrainingPipeline class..")
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            logging.info("Data validation completed successfully.")
        except Exception as e:
            raise CustomException(e, sys) from e