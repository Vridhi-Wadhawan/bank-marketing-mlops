# Bank Marketing Prediction API (MLOps)

This project is an end-to-end MLOps workflow where a machine learning model is trained, containerized, and deployed as a production-ready REST API.

The system predicts whether a bank customer is likely to subscribe to a term deposit based on marketing campaign data, enabling more targeted and efficient outreach.

---

## Project Highlights

- Built a complete ML pipeline: data preparation → modeling → inference
- Deployed a prediction service using Flask and Docker
- Exposed model predictions via a REST API
- Deployed and tested on cloud infrastructure (AWS EC2)

---

## Business Context

Marketing campaigns often suffer from low conversion rates due to untargeted outreach.  
This project addresses that by predicting customer subscription likelihood, helping prioritize high-probability leads and reduce ineffective contact attempts.

---

## Model & Pipeline Overview

- Model: K-Nearest Neighbors (KNN)
- Data: UCI Bank Marketing Dataset
- Preprocessing:
  - Feature engineering
  - Categorical encoding
  - Numerical scaling
- Output:
  - Binary prediction (Yes / No)
  - Class probabilities

---

## Tech Stack

- Python
- scikit-learn
- Flask
- Docker & Docker Compose
- AWS EC2

---

## Repository Structure

- `ML_Ops.ipynb` – Model training and experimentation
- `ML_Ops_App.ipynb` – API logic and inference flow
- `Dockerfile` – Container configuration
- `requirements.txt` – Python dependencies
- `deployment-process.md` – Detailed deployment steps and execution log

---

## Deployment & Execution Notes

Detailed deployment steps, commands, and cloud setup are documented separately in **`deployment-process.md`**.

---

## Notes

This repository focuses on demonstrating production-oriented machine learning practices rather than model benchmarking alone.
