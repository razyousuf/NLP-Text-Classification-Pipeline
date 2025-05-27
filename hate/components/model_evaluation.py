import os
import sys
import keras
import pickle
import pandas as pd
from hate.logger import logging
from hate.exception import CustomException
from keras.utils import pad_sequences
from hate.constants import *
from hate.configuration.gcloud_syncer import GCloudSync
from sklearn.metrics import confusion_matrix, roc_auc_score, precision_recall_curve
from hate.entity.config_entity import ModelEvaluationConfig
from hate.entity.artifact_entity import ModelEvaluationArtifacts, ModelTrainerArtifacts, DataTransformationArtifact


class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 model_trainer_artifacts: ModelTrainerArtifacts,
                 data_transformation_artifacts: DataTransformationArtifact):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts
        self.gcloud = GCloudSync()

    def get_best_model_from_gcloud(self) -> str:
        try:
            logging.info("Entered the get_best_model_from_gcloud method of Model Evaluation class")
            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)

            self.gcloud.sync_folder_from_gcloud(
                self.model_evaluation_config.BUCKET_NAME,
                self.model_evaluation_config.MODEL_NAME,
                self.model_evaluation_config.BEST_MODEL_DIR_PATH
            )

            best_model_path = os.path.join(
                self.model_evaluation_config.BEST_MODEL_DIR_PATH,
                self.model_evaluation_config.MODEL_NAME
            )
            logging.info("Exited the get_best_model_from_gcloud method of Model Evaluation class")
            return best_model_path
        except Exception as e:
            raise CustomException(e, sys) from e

    def evaluate(self, model, tokenizer):
        try:
            logging.info("Entering evaluate method of ModelEvaluation class")
            x_test = pd.read_csv(self.model_trainer_artifacts.x_test_path, index_col=0)
            y_test = pd.read_csv(self.model_trainer_artifacts.y_test_path, index_col=0)

            x_test = x_test['tweet'].astype(str).squeeze()
            y_test = y_test.squeeze()

            test_sequences = tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix = pad_sequences(test_sequences, maxlen=MAX_LEN)
            logging.info(f"test_sequences_matrix shape: {test_sequences_matrix.shape}")
            logging.info(f"y_test shape: {y_test.shape}")

            logging.info("Starting model.evaluate()")
            accuracy = model.evaluate(test_sequences_matrix, y_test, verbose=1)
            logging.info(f"Evaluation accuracy: {accuracy}")

            # Predict scores (sigmoid outputs)
            logging.info("Starting model.predict()")
            lstm_prediction = model.predict(test_sequences_matrix, verbose=1)
            logging.info("Finished model.predict()")

            # ROC-AUC
            roc_auc = roc_auc_score(y_test, lstm_prediction)
            logging.info(f"ROC AUC score: {roc_auc}")

            # Precision-recall curve
            precision, recall, thresholds = precision_recall_curve(y_test, lstm_prediction)

            # Compute F1 scores for all thresholds
            f1_scores = 2 * (precision * recall) / (precision + recall + 1e-6)
            best_threshold = thresholds[f1_scores.argmax()]
            logging.info(f"Best F1 score: {f1_scores.max():.4f} at threshold: {best_threshold:.4f}")

            # Save best threshold alongside model
            threshold_path = os.path.join(os.path.dirname(TRAINED_MODEL_DIR),"threshold.txt")
            with open(threshold_path, 'w') as f:
                f.write(str(best_threshold))
            logging.info(f"Saved best threshold to: {threshold_path}")
           
            # Convert predictions to binary labels
            res = [1 if p[0] >= 0.5 else 0 for p in lstm_prediction]

            cm = confusion_matrix(y_test, res)
            logging.info(f"Confusion Matrix: \n{cm}")
            print(cm)

            return accuracy[1]  # assuming accuracy is the second element
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        try:
            logging.info("Initiating model evaluation")

            logging.info("Loading trained model and tokenizer")
            trained_model = keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)

            trained_model_accuracy = self.evaluate(trained_model, tokenizer)

            best_model_path = self.get_best_model_from_gcloud()

            if not os.path.isfile(best_model_path):
                is_model_accepted = True
                logging.info("No best model found in GCloud. Accepting trained model.")
            else:
                logging.info("Evaluating best model from GCloud")
                best_model = keras.models.load_model(best_model_path)
                best_model_accuracy = self.evaluate(best_model, tokenizer)

                if trained_model_accuracy > best_model_accuracy:
                    is_model_accepted = True
                    logging.info("Trained model is better. Accepting trained model.")
                else:
                    is_model_accepted = False
                    logging.info("Best model is better. Rejecting trained model.")

            model_evaluation_artifacts = ModelEvaluationArtifacts(is_model_accepted=is_model_accepted)
            logging.info("Returning ModelEvaluationArtifacts")
            return model_evaluation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
