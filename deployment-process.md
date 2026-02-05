# Bank Marketing Prediction API – MLOps Deployment
## Deployment Process Document
==============================================================
PROJECT OVERVIEW
==============================================================
This project demonstrates an end-to-end MLOps workflow to deploy a machine learning model as a REST API. It includes:

- Docker containerization  
- Model training, serialization, and feature engineering  
- Deployment to AWS EC2  
- Prediction serving with Flask

==============================================================
BUSINESS OBJECTIVE
==============================================================
The goal of this project is to predict whether a bank customer will subscribe to a term deposit based on marketing campaign data. This allows the bank to:

- Optimize marketing efforts
- Focus resources on likely responders
- Improve conversion rates

==============================================================
DATASET AND STATISTICAL INSIGHTS
==============================================================
Dataset:  
- Bank Marketing Dataset (UCI)  
- 20+ features including:
  - Demographics (age, job, marital, education)
  - Campaign information (contact type, duration, previous outcome)
  - Economic indicators (emp.var.rate, cons.price.idx, euribor3m)

Target Variable Distribution:
- No subscription: ~89%
- Subscription: ~11%

Key Statistical Insights:
- Customers with previous contacts have higher subscription rates.
- Contact duration is positively correlated with conversion.
- Economic conditions (euribor3m) influence success probability.

==============================================================
FINAL MODEL AND INFERENCE
==============================================================
Model Used:
- K-Nearest Neighbors Classifier
- Preprocessing Pipeline includes:
  - Feature engineering (is_risk_group, season_category)
  - Encoding categorical variables
  - Scaling numeric features

Inference Output:
- Binary prediction: 0 = No, 1 = Yes
- Probability of each class

Example response:
{
  "prediction": 0,
  "prediction_proba_no": 1.0,
  "prediction_proba_yes": 0.0
}

==============================================================
LOCAL DEPLOYMENT
==============================================================
Note: Local deployment done on Gooel Cloud Shell as Docker desktop causing laptop to crash 

1. Upload following files on Google Cloud Shell
	- app.py                                  
	- bank_marketing_prep_pipeline.joblib  
	- Dockerfile  
	- sample.json
	- bank_marketing_k-nearest_neighbors.pkl  
	- docker-compose.yml                   
	- ml_ops.py   
	- requirements.txt

2. Verify if the files were loaded
ls

3. Build the Docker Image
docker compose build

4. Run the Container
docker compose up -d

5. Verify It's Running
docker ps

6. Test the API
curl http://localhost:5000/

7. Test a prediction:
curl -X POST -H "Content-Type: application/json" -d @sample.json http://localhost:5000/predict

8. Stop the container
docker compose down

9. Restart Later
docker compose up -d

10. Clean Up Everything
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)

**************************************************************
AMAZON WEB SERVICES (AWS) DEPLOYMENT
**************************************************************
==============================================================
1. AWS EC2 SETUP
==============================================================
1. Log in to AWS Console
- Navigate to EC2 Dashboard.

2. Launch a new instance
- AMI:Ubuntu Server 22.04 LTS (Free tier eligible)
- Instance Type: t2.micro
- Key Pair: Create a new key pair (.pem) and download it
- Storage: 8 GB (default)
- Security Group:
    - SSH (TCP 22): My IP
    - Custom TCP (TCP 5000): 0.0.0.0/0 (for API access)

3. Launch instance
- Wait for instance to be in Runningstate.
- Copy the Public IPv4 address.
- IPv4 Key: 43.204.221.151

==============================================================
2. TRANSFER PROJECT FILES
==============================================================
From your Windows Command Prompt:

scp -i "C:\Users\V\Downloads\mlops-key.pem" -r "C:\Users\V\Desktop\mlops\Assignment\Final\Local Deployment Final\AWS_Docker_Deployment" ubuntu@<PUBLIC_IP>:/home/ubuntu/
scp -i "C:\Users\V\Downloads\mlops-key.pem" -r "C:\Users\V\Desktop\mlops\Assignment\Final\Local Deployment Final\AWS_Docker_Deployment" ubuntu@43.204.221.151:/home/ubuntu/

This copies all project files into:
 /home/ubuntu/AWS_Docker_Deployment

==============================================================
2. CONNECT TO EC2 VIA SSH
==============================================================
From Windows Command Prompt:
ssh -i "C:\Users\V\Downloads\mlops-key.pem" ubuntu@<PUBLIC_IP>
ssh -i "C:\Users\V\Downloads\mlops-key.pem" ubuntu@43.204.221.151

First connection will ask to confirm fingerprint—type `yes`.

Verifying the file is copied 
ls

Changing Directories
cd "AWS_Docker_Deployment"

==============================================================
3. INSTALL DOCKER
==============================================================

Inside EC2 terminal:

Update package lists
sudo apt update -y

Install necessary packages for adding repositories
sudo apt install ca-certificates curl gnupg -y

Create the directory for keyrings if it doesn't exist
sudo install -m 0755 -d /etc/apt/keyrings

Download and add Docker's official GPG key
The output should be 'OK' or nothing if successful
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gp

Set appropriate permissions for the GPG key
sudo chmod a+r /etc/apt/keyrings/docker.gpg

Add the Docker repository to your apt sources list
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

Update apt package index again to include the new Docker repository
sudo apt update -y

Install the Docker Compose Plugin
sudo apt install docker-compose-plugin -y

Start Docker daemon
sudo systemctl start docker

Add your user to the docker group
sudo usermod -aG docker $USER

Verify Docker:
docker --version
docker version
docker compose version

==============================================================
5. BUILD AND RUN DOCKER
==============================================================
Inside EC2:

Changing Directories
cd "AWS_Docker_Deployment"

Checking all the existing dockers
docker ps -a

Stopping the existing dockers
docker stop <docker_name>

Removing the existing dockers
docker rm <docker_name>
docker rm bank_marketing_api
Build Docker:
docker compose build
(Ignore the `version` warnings)

Start container:
docker compose up -d

Verify running container:
docker ps

Should show:
0.0.0.0:5000->5000/tcp

==============================================================
6. TESTING THE API
==============================================================
Check that server is running:
curl http://localhost:5000/

Expected:
Bank Marketing Prediction REST API is running.

Test prediction:
curl -X POST -H "Content-Type: application/json" -d @sample.json http://localhost:5000/predict

Expected JSON response with prediction probabilities.

==============================================================
7. STOPPING AND RESTARTING
==============================================================

Stop container:
docker compose down

Restart container:
docker compose up -d

Stop EC2 instance to save costs:
AWS Console > EC2 > Instances > Actions > Instance State > Stop

(Note: Public IP may change after restart.)

==============================================================
8. DEPLOYMENT VERIFICATION CHECKLIST
==============================================================
- Docker image built successfully  
- Flask API responds to GET requests  
- API processes JSON input and returns prediction  
- Tested end-to-end via curl commands  
- Security Group allows external access to port 5000
