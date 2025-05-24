# Getting data from -and saving to- the GCloud bucket.
import os
import sys
from zipfile import ZipFile
from hate.logger import logging
from hate.exception import CustomException
from hate.configuration.gcloud_syncer import GCloudSync
from hate.entity.config_entity import DataIngestionConfig
from hate.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.gcloud_syncer = GCloudSync()

    def get_data_from_gcloud(self) -> None:
        try:
            logging.info("Entering the get_data_from_gcloud method of the DataIngestion class..")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.gcloud_syncer.sync_folder_from_gcloud(
                self.data_ingestion_config.BUCKET_NAME,
                self.data_ingestion_config.ZIP_FILE_NAME,
                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR
            )
            logging.info("Exiting the get_data_from_gcloud method of the DataIngestion class..")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def unzip_and_clean(self):
        logging.info("Entering the unzip_data method of the DataIngestion class..")
        try:
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            logging.info("Exiting the unzip_data method of the DataIngestion class..")
            return self.data_ingestion_config.DATA_ARTIFACTS_DIR, self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entering the initiate_data_ingestion method of the DataIngestion class..")
        try:
            self.get_data_from_gcloud()
            logging.info("Data downloaded from GCloud successfully.")
            imbalance_data_file_path, raw_data_file_path = self.unzip_and_clean()
            logging.info("Data unzipped and and split into train and validation.")

            data_ingestion_artifact = DataIngestionArtifact(
                imbalance_data_file_path=imbalance_data_file_path,
                raw_data_file_path=raw_data_file_path
            )
            logging.info("Exiting the initiate_data_ingestion method of the DataIngestion class..")
            logging.info(f"Data Ingestion Artifact paths: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys) from e

