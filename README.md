# 🏥 Diabetes Health Indicators

**Diabetes** is among the most prevalent chronic diseases in the United States, impacting millions of Americans each year and exerting a significant financial burden on the economy. 
**Diabetes** is a serious chronic disease in which individuals lose the ability to effectively regulate levels of glucose in the blood, and can lead to reduced quality of life and life expectancy.

* Dataset used can be found , [here](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset?resource=download&select=diabetes_binary_health_indicators_BRFSS2015.csv) (`diabetes_binary_health_indicators_BRFSS2015.csv`).

> Download the dataset used in this project, [here](https://storage.googleapis.com/kaggle-data-sets/1703281/2789260/compressed/diabetes_binary_health_indicators_BRFSS2015.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20241118%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20241118T134800Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=2c7aa1aba46693d3ce0644923c0968f768ae118b26566c8014a092cb8bc5943688d16f1dce02ff95922e11ff11495259e796fdc226a90a4ed8f3f8bea2c3517b0a474e57a0d3856c981bd346fa7de3da7a28c900f501c9b4afd14e4144ce7cc5049eb98c628f7316c8e983228c6596ff0ef54a1389cd1efa7fc905cc6fb92ffedc4970e35cca124129ae0c78b12dcabf9bc7636e4f97b8fecf5e6f58c8c09c98ebfe7341a7cd7c4b29ed094ca506bb533284b9fd4a54738918a57593cee8b11d5a26bf970289991ac86cec9b40a4cdebb39984211c9c25bb2d8c38d18fe91b458e0d45fc5dfb54b2e0eb2759afe6dee5f2722ac9f75e41e17b266824bf8d5daa)

### Table of contents

1. [⚙ Dependencies](#dependencies)
2. [📌 How to use this project](#how-to-use)
3. [👩🏼‍💻 Describing the construction of the project](#describe) <br> 
  3.1 [Data Versioning](#data-versioning) <br> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.1.a [Upload the dataset file in a S3 Bucket](#data-versioning-1) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.1.b [Configure data versioning - DVC](#data-versioning-2) <br>
  3.2 [Sagemaker](#sagemaker) <br> 
  3.3 [CI-CD](#ci-cd) <br>
  3.4 [Documentation](#doc)<br>
  3.5 [Logging](#log)<br>
  3.6 [Tracking](#mlfow)<br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.6.a [Centralization](#mlfow-1) <br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.6.a [Model Registry](#mlfow-2) <br>
  3.7 [Monitoring](#data-drift) <br>
  3.8 [ECR and Docker Image](#ecr-docker) <br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.8.a [Test docker image locally](#ecr-docker-1) <br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.8.b [Upload docker image in ECR container](#ecr-docker-2) <br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.8.c [Create Lambda Function from the image in ECR](#ecr-docker-3) <br>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3.8.d [Test endpoint](#ecr-docker-4) <br>

## ⚙ Dependencies <a name="dependencies"></a>

Create a `venv` and install dependencies:

```bash
    # Create environment
    $ python3 -m venv venv  

    # Activate environment
    $ source venv/bin/activate

    # Install dependencies
    $ pip install -r requirements.txt
``` 

Configure the secrets in your repository : go to the repository site on `github / settings / Secrets and variables / Actions` and add a **new repository secrets**.

Set all the secrests :

* `AWS_ACCESS_KEY_ID` (AWS credentials)
  
* `AWS_SECRET_ACCESS_KEY` (AWS credentials)
  
* `AWS_REGION` (AWS credentials)
  
* `AWS_LAMBDA_ROLE_ARN` (AWS credentials)

* `DB_USERNAME` (MlFlow)

* `DB_PASSWORD` (MlFlow)

* `DB_HOST` (MlFlow)

Also create a `config/.env` file with the following:

```bash
    AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
    AWS_SECRET_ACCESS_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaa"
    AWS_REGION="xx-xxxx-2"
    AWS_ACCOUNT_ID="XXXXXXXXXX"
    AWS_LAMBDA_ROLE_ARN="arn:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
``` 

Configure your AWS credentials:

```bash
    aws configure
```

## 📌 How to use this project <a name="how-to-use"></a>

Project variables can be found at file: `src/variables.py`.

To run the scripts locally:

```bash
 # Root folder 
 $ python -m src.preprocess
```

```bash
 # Root folder 
 # Terminal 1
 $ mlflow server --backend-store-uri postgresql://USERNAME:PASSWORD@HOST:5432/mlops_project_diabetes_db \
  --default-artifact-root s3://mlops-project-diabetes-tracking-bucket
 # Terminal 2
 $ python -m src.train
 # Access MLFlow  http://localhost:5000/
```

Test the deployed API :

```bash 
 $ curl -X POST -H "Content-Type: application/json" \
    -d '{"health_info": {"HighBP": 0.0, "HighChol": 1.0, "CholCheck": 1.0, "BMI": 40.0, "Smoker": 1.0, "Stroke": 0.0, "HeartDiseaseorAttack": 0.0, "PhysActivity": 0.0, "Fruits": 0.0, "Veggies": 0.0, "HvyAlcoholConsump": 1.0, "AnyHealthcare": 0.0, "NoDocbcCost": 1.0, "GenHlth": 0.0, "MentHlth": 5.0, "PhysHlth": 18.0, "DiffWalk": 15.0, "Sex": 1.0, "Age": 0.0, "Education": 9.0, "Income": 4.0}}' \
    <api-endpoint>/predict
```

Run tests:
```bash
 # Root folder
 $  pytest
```


## 👩🏼‍💻 Describing the construction of the project <a name="describe"></a>

### 1. Data Versioning <a name="data-versioning"></a>

#### 1.1 Upload the dataset file in a S3 Bucket <a name="data-versioning-1"></a>

```bash
   # With .csv inside data folder
   # Root folder
   $ python -m src.utils.upload_data
   # After that delete .csv in data folder
```

After this the URL of the file upload is : `https://<bucket-name>.s3.<region>.amazonaws.com/<key>`

> Data URL =  `https://mlops-project-diabetes-data-bucket.s3.us-east-2.amazonaws.com/diabetes_binary_health_indicators_BRFSS2015.csv`

```bash
  # Check files in bucket
  $ aws s3 ls s3://mlops-project-diabetes-data-bucket/
  # Check if the file is acessible
  $ curl -O https://mlops-project-diabetes-data-bucket.s3.us-east-2.amazonaws.com/diabetes_binary_health_indicators_BRFSS2015.csv
```

#### 1.2 Configure data versioning - [DVC](https://dvc.org/) <a name="data-versioning-2"></a>

```bash
 # Init dvc repository
 $ dvc init
 
 # Pre-signed URL for access the private bucket 
 $ aws s3 presign s3://mlops-project-diabetes-data-bucket/diabetes_binary_health_indicators_BRFSS2015.csv
 $ dvc get-url <generated-presigned-url> data/diabetes_data.csv

 # dvc to track data/
 $ dvc add data/diabetes_data.csv
```

Create a dvc bucket:

```bash
 # Create dvc bucket
 # Root folder
 $ python -m src.utils.create_dvc_bucket
 
 # Check if bucket was created
 $ aws s3 ls 
```

Add S3 in dvc:

```bash
  $ dvc remote add myremote s3://mlops-project-diabetes-dvc-bucket
  $ dvc remote default myremote
  $ dvc push
  
  # Check if myremote was add:
  $ dvc remote list
  
  # Check if the file was upload in bucket sync with dvc:
  $ dvc status
  $ aws s3 ls s3://mlops-project-diabetes-dvc-bucket/files/ --recursive
  
  # I you want you can delete the diabetes_data.csv and check if dvc restore the file 
  $ rm -rf data/diabetes_data.csv
  $ dvc pull # Check the file data/diabetes_data.csv been restaured
```

### 2. Sagemaker (Exploratory Analysis) <a name="sagemaker"></a>

Create a notebook instance to use :

```bash 
 # ROLE_ARN that have permission for Sagemaker in AWS (possible the value in config/.env file)
 $ aws sagemaker create-notebook-instance \
                    --notebook-instance-name "mlops-project-diabetes-exp-note" \
                    --role-arn "ROLE_ARN" \
                    --instance-type "ml.t2.medium" \
                    --volume-size-in-gb 10

 # Wait unil Status change to "InService"
 $ aws sagemaker describe-notebook-instance --notebook-instance-name "mlops-project-diabetes-exp-note"
 
 # Access the Url returned form this command on browser
```
For this project, the notebooks are in : https://mlops-project-diabetes-exp-note-hgae.notebook.us-east-2.sagemaker.aws/lab

The jupyter notebook in AWS Sagemaker with the exploratory analysis was downloaded to the `src/notebooks` folder.

### 3. Configure CI-CD (Github workflows) <a name="ci-cd"></a>

The `.github/workflows/workflow.yaml` folder contains the file with the pipeline sets and stages.

> [!WARNING] 
> 
> Before any commit that triggers the pipeline is made, it is necessary to update the DVC repository
> ```bash
>   $ dvc status
>   $ dvc pull
> ```

`Preprocess Stage`: Prepares data that will be used in model training

`Monitoring Stage`: Monitors data that will be used by the Logistic Regression model to check if there has been any data drift

`Train Stage`: Train the logistic regression model

`Predict Stage`: Creates a lambda function that predicts the model. Also create an API gateway to access this function

`Test Stage`: Tests the data preprocessing and model training processes and also tests whether the API is returning status 200 when requested.

### 4. Documentation <a name="doc"></a>

**Sphinx**  generate auto documentation for the project. 

```bash
  # If any change on docs/ folder rebuild the documentation:
  $ cd docs/ && make html 
```

To access the project documentation open the file : `docs/_build/html/index.html`

### 5. Logging (S3 Bucket) <a name="log"></a>

All project logs are stored within an **S3 bucket**.

The class responsible for instantiating this bucket can be found at: `src/dataclass/bucket/log_bucket.py`.

The log level can be configured at: `src/dataclass/log_manager.py` using `set_baseConfig(log_level)` function.

Buckets storing project log information:

* `preprocess.py`: 
  * **bucket_name = mlops-project-diabetes-log-bucket**
  * **key = mlops-project-diabetes-preprocess-logs** 
  * **logger_name = process_logger**
 
* `train.py`: 
  * **bucket_name = mlops-project-diabetes-log-bucket**
  * **key = mlops-project-diabetes-train-logs** 
  * **logger_name = train_logger** 

### 6. Tracking (MlFlow) <a name="mlfow"></a>

#### 6.1 Centralization <a name="mlfow-1"></a>

Information about the model is saved so that everyone can see it.

```bash
     |_Database_| ↔️  |_MLFOW_Server_| ↔️  |_S3_Bucket_|
                            ↕️ 
                    |_ML_Model_Code_|
```  

##### 6.1.a Database created with name = **mlops_project_diabetes_db <a name="mlfow-1-a"></a>

In a postgres script run:

```sql
CREATE DATABASE mlops_project_diabetes_db;
SELECT datname FROM pg_database; -- Expected the database name
```

##### 6.1.b Bucket create with name = **mlops-project-diabetes-tracking-bucket <a name="mlfow-1-b"></a>

```bash
  $ aws s3api create-bucket --bucket mlops-project-diabetes-tracking-bucket \
  --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2
  # LOCATION: http://mlops-project-diabetes-tracking-bucket.s3.amazonaws.com/
  
  # Check if bucket was created
  $ aws s3 ls
```

##### 6.1.c Run MlFlow server to use information from Database and the S3 bucket created <a name="mlfow-1-c"></a>

```bash
  # Terminal 1
  $ mlflow server --backend-store-uri postgresql://USERNAME:PASSWORD@HOST:5432/mlops_project_diabetes_db \
  --default-artifact-root s3://mlops-project-diabetes-tracking-bucket
```

> username , password , host and port = 5432 are the database credentials.

In another terminal run the training: 

```bash
  # Terminal 2
  # Root folder
  $ python -m src.train
```

#### 6.2 Model Registry <a name="mlfow-2"></a>

Run a specific model version locally using Docker:
```bash
  $ export MLFLOW_TRACKING_URI=http://localhost:5000
  $ mlflow models build-docker --name <model-name> --model-uri "models:/<model-name>/<version>"
  # Models tab in MLFlow has <model-name> and <version> of registered model
  $ docker run -d -p 8080:8080 <model-name>:latest
  # In another terminal you can make requests passing a new data and receiving the prediction
```

### 7. Monitoring (Data Drift) <a name="data-drift"></a>

To assess whether there was data drift with the data, run:

```bash
  # Root folder
  $ python -m src.monitoring.data_drift
```

### 8. ECR and Docker Image <a name="ecr-docker"></a>

#### 8.1 Test docker image locally <a name="ecr-docker-1"></a>
 
```bash
  # Root
  # Terminal 1
  $ docker build --platform linux/amd64 -t <image-name>:<tag> .
  # docker build --platform linux/amd64 -t lambda-ex-image:test .
  
  $ docker run -p 9500:8080 <image-name>:<tag>
  # docker run -p 9500:8080 lambda-ex-image:test

  # Root
  # Terminal 2
  $ curl -X POST "http://localhost:9500/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{"body": "{\"health_info\": {\"HighBP\": 0.0, \"HighChol\": 1.0, \"CholCheck\": 1.0, \"BMI\": 40.0, \"Smoker\": 1.0, \"Stroke\": 0.0, \"HeartDiseaseorAttack\": 0.0, \"PhysActivity\": 0.0, \"Fruits\": 0.0, \"Veggies\": 0.0, \"HvyAlcoholConsump\": 1.0, \"AnyHealthcare\": 0.0, \"NoDocbcCost\": 1.0, \"GenHlth\": 0.0, \"MentHlth\": 5.0, \"PhysHlth\": 18.0, \"DiffWalk\": 15.0, \"Sex\": 1.0, \"Age\": 0.0, \"Education\": 9.0, \"Income\": 4.0}}"}'
```
#### 8.2 Upload docker image in ECR container <a name="ecr-docker-2"></a>

Create repository:
```bash
 $ python -m src.utils.create_docker_container
 # Repository URI: 820926566402.dkr.ecr.us-east-2.amazonaws.com/mlops-project-diabetes-ecr
```

Authenticate and login to ECR using the Docker CLI:
```bash
 $ aws ecr get-login-password --region <REGION> --profile mlops | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
 # aws ecr get-login-password --region us-east-2 --profile mlops | docker login --username AWS --password-stdin 820926566402.dkr.ecr.us-east-2.amazonaws.com
```

```bash
 $ docker tag <image-name>:<tag> <repository-uri>:latest
 # docker tag lambda-ex-image:test 820926566402.dkr.ecr.us-east-2.amazonaws.com/mlops-project-diabetes-ecr:latest
 
 $ docker push <repository-uri>:latest
 # docker push 820926566402.dkr.ecr.us-east-2.amazonaws.com/mlops-project-diabetes-ecr:latest
 
 # Check repository content:
 $ aws ecr describe-images --repository-name mlops-project-diabetes-ecr
```

#### 8.3 Create Lambda Function from the image in ECR <a name="ecr-docker-3"></a>

Create lambda function:

```bash
 $ python -m src.utils.create_lambda_function
 # Function ARN: arn:aws:lambda:us-east-2:820926566402:function:mlops-project-diabetes-lambda-function
```

Create api to access lambda function:
```bash
 $ python -m src.utils.create_api
 # API Endpoint : https://gn5battgc1.execute-api.us-east-2.amazonaws.com
```
#### 8.4 Test endpoint <a name="ecr-docker-4"></a>

```bash
 $ curl -X POST -H "Content-Type: application/json" \
    -d '{"health_info": {"HighBP": 0.0, "HighChol": 1.0, "CholCheck": 1.0, "BMI": 40.0, "Smoker": 1.0, "Stroke": 0.0, "HeartDiseaseorAttack": 0.0, "PhysActivity": 0.0, "Fruits": 0.0, "Veggies": 0.0, "HvyAlcoholConsump": 1.0, "AnyHealthcare": 0.0, "NoDocbcCost": 1.0, "GenHlth": 0.0, "MentHlth": 5.0, "PhysHlth": 18.0, "DiffWalk": 15.0, "Sex": 1.0, "Age": 0.0, "Education": 9.0, "Income": 4.0}}' \
    <api-endpoint>/predict
```

The test on the `tests/endpoint_test.py` also checks the function endpoint.


<div align="center">
    <br>
    @2024, Insper. 9° Semester, Computer Engineering.<br>
    Machine Learning Ops & Interviews Discipline
</div>
