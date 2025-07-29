# MLOps Translation App

A full-stack MLOps project demonstrating **CI/CD**, **blue-green deployment**, and **ML monitoring** with **Jenkins**, **Ansible**, **Docker**, **React**, **FastAPI**, and **MLflow**.

## Project Structure
mlops-translation-app/
│
├── backend/ # FastAPI backend (ML model + API)
│ ├── main.py
│ ├── translator.py
│ ├── requirements.txt
│ └── mlflow_logs/ # MLflow logs directory
│
├── frontend/ # React frontend (Translation UI)
│
├── ansible/ # Ansible playbooks for deployment
│ ├── blue_green_deploy.yml
│ └── inventory.ini
│
├── Jenkinsfile # Jenkins pipeline script
└── nginx/ # NGINX reverse proxy config

## Features

- **React frontend** with user-friendly interface
- **FastAPI backend** with deployed ML model
- **MLflow UI** for experiment tracking
- **Docker Compose** for multi-container orchestration
- **Blue-Green Deployment** using Ansible
- **CI/CD** pipeline via Jenkins
- **Webhook-triggered deployment** on code push

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/nirav2292001/mlops-translation-app.git
cd mlops-translation-app
```

### 2. Run Locally via Docker Compose

```bash
docker-compose up --build -d
```

### 3. Access the App

| Service     | URL                                                      |
| ----------- | -------------------------------------------------------- |
| Frontend UI | [http://localhost](http://localhost)                     |
| Backend API | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Jenkins UI  | [http://localhost:8080](http://localhost:8080)           |
| MLflow UI   | [http://localhost:5000](http://localhost:5000)           |

## Blue-Green Deployment

Handled by Ansible from Jenkins pipeline.

Command (via Jenkins or manually):
```bash
cd ansible/
ansible-playbook -i inventory.ini blue_green_deploy.yml
```
Creates new frontend container (frontend-green)

Updates NGINX to point to green or blue

Ensures zero-downtime switching

## CI/CD Pipeline

Triggered via GitHub Webhook

Executes the Jenkinsfile

Pulls latest code → builds → deploys using Ansible

Webhook endpoint:

```
http://<JENKINS_IP>:8080/generic-webhook-trigger/invoke
```

## MLflow Integration

The backend logs experiments to MLflow:

UI on port 5000

Backend logs under mlflow_logs/

Run manually in backend:

```bash
mlflow ui --backend-store-uri ./mlflow_logs --host 0.0.0.0 --port 5000
```
(Already handled in Docker setup)

## Technology Stack

| Layer    | Technology                    |
| -------- | ----------------------------- |
| Frontend | React.js                      |
| Backend  | FastAPI + ML model            |
| DevOps   | Docker, Jenkins, Ansible      |
| MLOps    | MLflow, Blue-Green Deployment |
| Infra    | NGINX, Docker Compose         |

## Author
Built with by Nirav Dhimmar