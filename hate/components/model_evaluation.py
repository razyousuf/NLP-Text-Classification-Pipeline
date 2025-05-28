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
    def __init__(self, model_evaluation_config: ModelEvaluationConfig, model_trainer_artifacts: ModelTrainerArtifacts, data_transformation_artifacts: DataTransformationArtifact):
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts
        self.gcloud = GCloudSync()
        try:
            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)
            logging.info(f"Created directory: {self.model_evaluation_config.BEST_MODEL_DIR_PATH}")
        except Exception as e:
            logging.warning(f"Could not create directory {self.model_evaluation_config.BEST_MODEL_DIR_PATH}: {e}")

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
            loss, accuracy = model.evaluate(test_sequences_matrix, y_test, verbose=1)
            logging.info(f"Evaluation Loss: {loss}, Evaluation Accuracy: {accuracy}")

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
            f1_scores_round = round(f1_scores.max(), 2)
            logging.info(f"Best F1 score: {f1_scores_round:.2f} at threshold: {best_threshold:.4f}")

            try:
                with open('threshold.txt', 'w') as f:
                    f.write(str(best_threshold))
                logging.info(f"Saved best threshold to the file.")
            except Exception as e:
                logging.warning(f"Failed to save best threshold: {e}")
                    
            # Convert predictions to binary labels
            res = [1 if p[0] >= best_threshold else 0 for p in lstm_prediction]

            cm = confusion_matrix(y_test, res)
            logging.info(f"Confusion Matrix: \n{cm}")
            print(cm)

            return loss, accuracy, f1_scores_round, best_threshold
        
        except Exception as e:
            raise CustomException(e, sys) from e


    import pandas as pd

    def save_metrics(self, model_name: str, loss: float, accuracy: float, f1_score: float, threshold: float):
        """
        Saves model evaluation metrics to a CSV file.

        :param model_name: Identifier for the model (e.g., 'trained_model', 'best_model')
        :param loss: Evaluation loss
        :param accuracy: Evaluation accuracy
        :param f1_score: F1 score
        :param threshold: Classification threshold used
        :param timestamp: Current timestamp
        :return: None
        """
        try:
            metrics_path = os.path.join(
                self.model_evaluation_config.BEST_MODEL_DIR_PATH, 
                self.model_evaluation_config.EVALUATION_METRICS_FILE
                )
            
            os.makedirs(os.path.dirname(metrics_path), exist_ok=True) # Create the above directory if it doesn't exist

            result_dict = {
                "model": model_name,
                "loss": loss,
                "accuracy": accuracy,
                "f1_score": f1_score,
                "threshold": threshold,
                "timestamp": pd.Timestamp.now()
            }

            df = pd.DataFrame([result_dict])
            if os.path.isfile(metrics_path):
                df_existing = pd.read_csv(metrics_path)
                df = pd.concat([df_existing, df], ignore_index=True)

            df.to_csv(metrics_path, index=False)
            logging.info(f"Saved evaluation metrics to: {metrics_path}")
            return

        except Exception as e:
            raise CustomException(e, sys) from e

    
    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        try:
            logging.info("Initiating model evaluation")

            logging.info("Loading trained model and tokenizer")
            trained_model = keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)

            trained_loss, trained_model_accuracy, trained_f1, trained_threshold = self.evaluate(trained_model, tokenizer)
            self.save_metrics("trained_model", trained_loss, trained_model_accuracy, trained_f1, trained_threshold)


            best_model_path = self.get_best_model_from_gcloud()

            if not os.path.isfile(best_model_path):
                is_model_accepted = True
                logging.info("No best model found in GCloud. Accepting trained model.")
            else:
                logging.info("Evaluating best model from GCloud")
                best_model = keras.models.load_model(best_model_path)
                best_model_loss, best_model_accuracy, best_model_f1, best_model_threshold = self.evaluate(best_model, tokenizer)
                #self.save_metrics("best_model", best_model_loss, best_model_accuracy, best_model_f1, best_model_threshold)
                if None in (best_model_loss, best_model_accuracy, best_model_f1, best_model_threshold):
                    logging.warning("Best model evaluation failed or returned None.")
                else:
                    self.save_metrics("best_model", best_model_loss, best_model_accuracy, best_model_f1, best_model_threshold)


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
