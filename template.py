import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

project_name = "hate"

list_of_files = [
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_transformatoin.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/gcloud_syncer.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/predictor.py",
    f"{project_name}/pipeline/trainer.py",
    f"{project_name}/ml/__init__.py",
    f"{project_name}/ml/model.py",
    "app.py",
    #"main.py",
    "requirements.txt",
    "demo.py",
    "Dockerfile",
    "setup.py",
    ".dockerignore",
]


for file_path in list_of_files:
    file_path = Path(file_path)

    filedir, file_name = os.path.split(file_path)

    # 1. Create the directory, if it does not exist
    if filedir != "": 
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {file_name}")
    
    # 2. Create the file if it does not exist or is empty
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
        logging.info(f"Creating an empty file: {file_name} in {file_path}")

    else:
        logging.info(f"File {file_name} already exists in {file_path}. Skipping creation.")