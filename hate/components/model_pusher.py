import sys
from hate.logger import logging
from hate.exception import CustomException
from hate.entity.artifact_entity import ModelPusherArtifact
from hate.entity.config_entity import ModelPusherConfig
from hate.configuration.gcloud_syncer import GCloudSync


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        """
        : param model_pusher_config: Configuration for the model pusher
        """
        self.model_pusher_config = model_pusher_config
        self.gcloud = GCloudSync()
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name:    Initiate_model_pusher
        Description:    Initiates the model pusher
        Output:         Returns the model pusher artifact
        On Failure:     Write an exception log and then raise an exception
        
        """
        try:
            # Upload model to gcloud
            self.gcloud.sync_folder_to_gcloud(
                self.model_pusher_config.BUCKET_NAME, 
                self.model_pusher_config.TRAINED_MODEL_PATH, 
                self.model_pusher_config.MODEL_NAME
                )
            logging.info("Model pushed to gcloud successfully.")
            
            # Saving the model pusher artifacts
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.BUCKET_NAME)
            logging.info("Exiting initiate_model_pusher method of the ModelPusher class..")
            return model_pusher_artifact
        
        
        except Exception as e:
            raise CustomException(e, sys) from e