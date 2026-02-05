# Bank Marketing Prediction API (MLOps)

This project demonstrates an end-to-end **Machine Learning Operations (MLOps)** workflow, where a predictive model is trained, containerized, and deployed as a production-ready REST API.

The system predicts whether a bank customer is likely to subscribe to a term deposit based on marketing campaign data, enabling more targeted and efficient outreach.

---

## Project Highlights

- Built a complete ML pipeline from data preparation to model inference  
- Developed a REST API for real-time predictions using Flask  
- Containerized the application using Docker for portability and consistency  
- Deployed and tested the service on cloud infrastructure (AWS EC2)

---

## Business Context

Bank marketing campaigns often experience low conversion rates due to broad, untargeted outreach.  
This project addresses the problem by predicting customer subscription likelihood, allowing marketing teams to prioritize high-probability leads and reduce ineffective contact attempts.

---

## Model & Pipeline Overview

- **Model:** K-Nearest Neighbors (KNN)
- **Dataset:** UCI Bank Marketing Dataset
- **Preprocessing:**
  - Feature engineering
  - Categorical variable encoding
  - Numerical feature scaling
- **Inference Output:**
  - Binary prediction (Subscribe / Not Subscribe)
  - Class-level probability scores

---

## System Architecture

![MLOps Architecture](/architecture.png)

**High-level flow:**
1. Raw marketing data is processed using a preprocessing pipeline  
2. The trained model and pipeline are serialized for inference  
3. A Flask-based API serves predictions  
4. The application is containerized using Docker  
5. The container is deployed on AWS EC2 for external access

---

## Tech Stack

- Python  
- scikit-learn  
- Flask  
- Docker & Docker Compose  
- AWS EC2  

---

## Repository Structure

- `ML_Ops.ipynb` – Model training, feature engineering, and evaluation  
- `ML_Ops_App.ipynb` – Inference logic and API integration  
- `Dockerfile` – Container build configuration  
- `requirements.txt` – Python dependencies  
- `deployment-process.md` – Detailed deployment steps and execution logs  

---

## API Usage (Minimal Example)

### Health Check
```bash
curl http://<EC2_PUBLIC_IP>:5000/
```

### Prediction Request
curl -X POST \
  -H "Content-Type: application/json" \
  -d @sample.json \
  http://<EC2_PUBLIC_IP>:5000/predict

### Sample Response
{
  "prediction": 0,
  "prediction_proba_no": 0.91,
  "prediction_proba_yes": 0.09
}

## Deployment Notes
Detailed cloud setup, Docker commands, and validation steps are documented in `deployment-process.md`.

## Final Note
This repository emphasizes production-oriented machine learning practices, focusing on deployment readiness, reproducibility, and real-world decision support rather than model benchmarking alone.
