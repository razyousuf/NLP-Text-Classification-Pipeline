import os
from keras.utils import pad_sequences

from hate.logger import logging
from hate.exception import CustomException

from hate.configuration.gcloud_syncer import GCloudSync
from hate.components.data_transformation import DataTransformation

from hate.entity.artifact_entity import DataIngestionArtifact
from hate.entity.config_entity import DataTransformationConfig


class PredictionPipeline:
    def __init__(self):
        self.gcloud_syncer = GCloudSync()
        self.data_transformation_config = DataTransformationConfig()
        self.data_transformation = DataTransformation(self.data_transformation_config)
