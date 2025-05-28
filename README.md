# NLP-Text-Classification-Pipeline

## Stages

1. Data Ingestion
2. Data Validation
3. Data Trnsformation
4. Model Training
5. Model Evaluation
6. Model Pusher
7. Model Prediction
8. Model Deployment

## Workflows

1. constants
2. config_entity
3. artifact_entity
4. components
5. pipeline
6. app.py

## Running the programme

```bash
conda create -n nlp python=3.10 -y
```

```bash
conda activate nlp
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

## Model Deployment setup

1. Setup the CircleCI
2. Activate the 'Self-Hosted Runners' by confirming the terms
3. Create a new project
4. Configure VM instance and GCR in GCP
5. Write the 'config.yml' file
6. setup the environment variables
