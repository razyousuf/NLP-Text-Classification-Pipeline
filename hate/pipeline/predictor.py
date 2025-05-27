import os
import sys

import pickle
import keras
from keras.utils import pad_sequences

from hate.logger import logging
from hate.exception import CustomException

from hate.constants import *
from hate.configuration.gcloud_syncer import GCloudSync
from hate.components.data_transformation import DataTransformation
from hate.entity.artifact_entity import DataValidationArtifact
from hate.entity.config_entity import DataTransformationConfig, ModelEvaluationConfig


class PredictionPipeline:
    def __init__(self):
        self.bucket_name = BUCKET_NAME 
        self.model_name = MODEL_NAME
        self.threshold_file = THRESHOLD_FILE_NAME
        self.model_path = os.path.join("artifacts", "PredictionModel")
        self.gcloud_syncer = GCloudSync()
        self.data_transformation_config = DataTransformationConfig()
        self.data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config, data_validation_artifact=DataValidationArtifact)
        self.model_evaluation_config = ModelEvaluationConfig()

    def get_model_from_gcloud(self) -> str:
        """
        Method Name:    get_model_from_gcloud
        Description:    Downloads the best model from gcloud storage
        Output:         Returns the best model path
        On Failure:     Write an exception log and then raise an exception
        """
        try:
            logging.info("Entering get_model_from_gcloud method of the PredictionPipeline class..")
            # Download the model from gcloud
            os.makedirs(self.model_path, exist_ok=True)
            self.gcloud_syncer.sync_folder_from_gcloud(self.bucket_name, self.model_name, self.model_path)
            best_model_path = os.path.join(self.model_path, self.model_name)
            logging.info(f"Model downloaded from gcloud successfully: {best_model_path}")
            return best_model_path

        except Exception as e:
            raise CustomException(e, sys) from e

    def predict(self, best_model_path: str, input_text) -> str:
        """
        Method Name:    predict
        Description:    Predicts the class of the input data
        Output:         Returns the predicted class
        On Failure:     Write an exception log and then raise an exception
        """
        try:
            logging.info("Entering predict method of the PredictionPipeline class..")
            # Get the model from gcloud
            model_file_check_path = best_model_path  # .h5 file
            if not os.path.isfile(model_file_check_path):
                best_model_path = self.get_model_from_gcloud()
            load_model = keras.models.load_model(best_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            
            text = self.data_transformation.concat_data_cleaning(input_text)
            text = [text]
            seq = tokenizer.texts_to_sequences(text)
            print(f"Input text after tokenization: {seq}")
            pad = pad_sequences(seq, maxlen=MAX_LEN)
            print(f"Input text after padding: {pad}")
            prediction = load_model.predict(pad)
            print(f"Prediction: {prediction}")
            score = float(prediction.squeeze())  # or prediction[0][0]

            threshold_file = os.path.join(self.model_evaluation_config.BEST_MODEL_DIR_PATH, self.model_evaluation_config.THRESHOLD_FILE_NAME)
            if not os.path.isfile(threshold_file):
                with open(threshold_file, "r") as f:
                    threshold = float(f.read())
                if score >= threshold:
                    print("Hate Speech Detected")
                    return "Hate Speech"
                else:
                    print("Not Hate Speech Detected")
                    return "Not Hate Speech"
            else:
                raise Exception(f"Threshold file not found at {threshold_file}. Please ensure the model evaluation step has been completed successfully.")
        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self, input_text: str):
        """
        Method Name:    run_pipeline
        Description:    Runs the prediction pipeline
        Output:         Returns the predicted class
        On Failure:     Write an exception log and then raise an exception
        """
        try:
            logging.info("Entering run_pipeline method of the PredictionPipeline class..")
            best_model_path = os.path.join(self.model_path, self.model_name)
            predicted_class = self.predict(best_model_path, input_text)
            return predicted_class
        
        except Exception as e:
            raise CustomException(e, sys) from e