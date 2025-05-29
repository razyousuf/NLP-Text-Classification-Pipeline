# NLP-Text-Classification-Pipeline

This is a modular, production-ready machine learning project for detecting hate speech in text data using deep learning. It follows a clean, stage-wise architecture with components for data ingestion, validation, transformation, model training, evaluation, and deployment. The pipeline includes GCP integration for cloud storage, model registry, and CI/CD with CircleCI for automated deployment on a GCP VM. This project ensures scalable, reproducible ML workflows suitable for real-world NLP applications.

## Pipeline Stages

1. Data Ingestion
2. Data Validation
3. Data Trnsformation
4. Model Training
5. Model Evaluation
6. Model Pusher
7. Model Prediction
8. Model Deployment

Note: You need to install and configure the gcloud sdk in your system to featch the data from gcloud storage bucket

## Workflows (For each stage in the pipeline)

1. constants
2. config_entity
3. artifact_entity
4. components
5. pipeline
6. main.py

## Model Deployment setup

1. Setup the CircleCI
2. Activate the 'Self-Hosted Runners' by confirming the terms
3. Create a new project in CircleCI
4. Link the project to your GitHub repository
5. Configure VM instance
6. Configure GCR in GCP
7. Write the 'config.yml' file
8. setup the environment variables

### a. Allow CircleCI to Clone Private GitHub Repository

1. Generate a dedicated SSH key pair for your project (on your local machine):

   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/project_key -C "your_email@example.com"
   ```

   - This generates two files:
     - ~/.ssh/project_key (private key)
     - ~/.ssh/project_key.pub (public key)

2. Add the public key to GitHub as a Deploy Key:
   - Go to your GitHub repo → Settings → Deploy Keys
   - Click "Add deploy key"
     - Title: e.g., CircleCI Access
     - Key: paste the contents of project_key.pub
     - Enable "Allow write access" if needed (e.g., if CircleCI pushes code/tags)
3. Add the private key to CircleCI:
   - Go to CircleCI Project Settings → SSH Keys → "Add SSH Key"
   - Choose: "Other"
     - Paste the private key (project_key)
     - Hostname: github.com

### b. GCP VM Setup for End-to-End Automation

1. Create a VM instance in GCP with a Linux OS (e.g., Ubuntu 22.04) and allow HTTP/HTTPS traffic.
2. Allow firewall rules to enable access port8080.
3. Enable Artifact Registry API in your GCP project to allow Docker image pulling.
4. Install Docker on the VM instance.
5. Authenticate Docker with Artifact Registry:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

6. Give the VM access to pull from Artifact Registry (via service account permissions or using gcloud auth login).
7. Install Google Cloud SDK on the VM (if not using a service account)
8. Add the docker user to admin group:

   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

9. Restart the VM to apply the changes.

### c. GCP VM SSH Setup & CircleCI Deployment

1. Create an SSH key pair on your local machine (if you don’t already have one):

```bash
$ ssh-keygen -t rsa -f ~/.ssh/gcp-key -C youremail@gmail.com
```

2. Add the public key to your GCP VM:
   - Go to the VM instance details in GCP.
   - Click "Edit" → scroll to SSH Keys.
   - Click "Add Key" → paste the public key from ~/.ssh/gcp-key.pub.
3. Add the private key to CircleCI:
   - Go to your project in CircleCI → Project Settings → SSH Keys → Add SSH Key.
   - Paste your private key (~/.ssh/gcp-key) there.
   - Set the hostname as 35.xxx.xxx.xxx (your VM's external IP) or just \*.
4. Add the GCP required environment variables in CircleCI environment variables:
   - Go to your project in CircleCI → Environment Variables → Add Environment Variable. e.g., for GCP VM IP:
   - Name: `GCP_VM_IP`, Value: `35.xxx.xxx.xxx`
   - Name: `SSH_PRIVATE_KEY`, Value: your private key (~/.ssh/gcp-key in base64) --> Follow the `config.yml` file for this important step.

## Running the programme locally

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
python main.py
```
