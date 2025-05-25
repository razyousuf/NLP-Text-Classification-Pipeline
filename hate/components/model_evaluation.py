import os
import sys
import pickle
import keras
import numpy as np
import pandas as pd

from hate.logger import logging
from hate.exception import CustomException

from keras.utils import pad_sequences
from sklearn.metrics import confusion_matrix
from hate.constants import *
from hate.configuration.gcloud_syncer import GCloudSync
from hate.entity.config_entity import ModelEvaluationConfig
from hate.entity.artifact_entity import ModelEvaluationArtifacts, ModelTrainerArtifacts, DataTransformationArtifact



class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig, model_trainer_artifacts: ModelTrainerArtifacts, data_transformation_artifact: DataTransformationArtifact):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifact = data_transformation_artifact
        
        self.gcloud_sync = GCloudSync()


    def get_model_from_gcloud(self) -> str:
        """
        : return: fetch the best model from the GCloud bucket and store inside best model folder
        """
        try:
            logging.info("Entered get_model_from_gcloud method of ModelEvaluation class")

            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)
            
            self.gcloud_sync.sync_folder_from_gcloud(
                self.model_evaluation_config.BUCKET_NAME,
                self.model_evaluation_config.MODEL_NAME,
                self.model_evaluation_config.BEST_MODEL_DIR_PATH
            )
            best_model_path = os.path.join(self.model_evaluation_config.BEST_MODEL_DIR_PATH, self.model_evaluation_config.MODEL_NAME)
            logging.info("Exited get_model_from_gcloud method of ModelEvaluation class")
            
            return best_model_path
        
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def evaluate_model(self):
        try:
            logging.info("Entered evaluate_model method of ModelEvaluation class")
            print(self.model_trainer_artifacts.x_test_path)

            x_test = pd.read_csv(self.model_trainer_artifacts.x_test_path, index_col=0)
            print(x_test.head())
            y_test = pd.read_csv(self.model_trainer_artifacts.y_test_path, index_col=0)

            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            load_model = keras.models.load_model(self.model_trainer_artifacts.trained_model_path)

            x_test = x_test['tweet'].astype(str)
            x_test = x_test.squeeze()
            y_test = y_test.squeeze()

            test_sequences = tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix = pad_sequences(test_sequences,maxlen=MAX_LEN)
            print(f"========{test_sequences_matrix}===========")
            print(f"========{x_test.shape}===========")

            accuracy = load_model.evaluate(test_sequences_matrix, y_test)
            logging.info(f"Test accuracy: {accuracy}")

            lstm_prediction = load_model.predict(test_sequences_matrix)
            
            result = []
            for prediction in lstm_prediction:
                if prediction[0] >= 0.5:
                    result.append(1)
                else:
                    result.append(0)

            print(confusion_matrix(y_test, result))
            logging.info(f"Confusion Matrix: {confusion_matrix(y_test, result)}")

            return accuracy
        except Exception as e:
            raise CustomException(e, sys) from e


    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        """
        Method Name: initiate_model_evaluation
        Description: initiate model evaluation
        Output: Returns the model evaluation artifact
        On failure: Write an exception log and then raise an exception
        """
        try:
            logging.info("Entered initiate_model_evaluation method of ModelEvaluation class")
            trained_model = keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                load_tokenizer = pickle.load(handle)

            trained_model_accuracy = self.evaluate_model()

            logging("Fetch the model from gcloud bucket") 
            best_model_path = self.get_model_from_gcloud()
            
            logging.info("Check if best model present in the gcloud bucket or not")
            if os.path.isfile(best_model_path) is False:
                is_model_accepted = True
                logging.info("gcloud bucket does not contain the model, and current trained model is accepted True")
            else:
                logging.info("Load the best model from the gcloud bucket")
                best_model = keras.models.load_model(best_model_path)
                best_model_accuracy = self.evaluate_model()
                logging.info("Check if the current trained model is better than the gcloud model (trained_model_loss & best_model_loss)")
                if best_model_accuracy > trained_model_accuracy:
                    is_model_accepted = True
                    logging.info("Trained model is not accepted")
                else:
                    is_model_accepted = False
                    logging.info("Trained model is accepted")

            model_evaluation_artifacts = ModelEvaluationArtifacts(is_model_accepted=is_model_accepted)
            logging.info("Exited initiate_model_evaluation method of ModelEvaluation class, and return model_evaluation_artifacts")
            return model_evaluation_artifacts
        except Exception as e:
            raise CustomException(e, sys) from e