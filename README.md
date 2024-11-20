## 🏥 Diabetes Health Indicators

**Diabetes** is among the most prevalent chronic diseases in the United States, impacting millions of Americans each year and exerting a significant financial burden on the economy. 
**Diabetes** is a serious chronic disease in which individuals lose the ability to effectively regulate levels of glucose in the blood, and can lead to reduced quality of life and life expectancy.

* Dataset used can be found , [here](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset?resource=download&select=diabetes_binary_health_indicators_BRFSS2015.csv) (`diabetes_binary_health_indicators_BRFSS2015.csv`).

> Download the dataset used in this project, [here](https://storage.googleapis.com/kaggle-data-sets/1703281/2789260/compressed/diabetes_binary_health_indicators_BRFSS2015.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20241118%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20241118T134800Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=2c7aa1aba46693d3ce0644923c0968f768ae118b26566c8014a092cb8bc5943688d16f1dce02ff95922e11ff11495259e796fdc226a90a4ed8f3f8bea2c3517b0a474e57a0d3856c981bd346fa7de3da7a28c900f501c9b4afd14e4144ce7cc5049eb98c628f7316c8e983228c6596ff0ef54a1389cd1efa7fc905cc6fb92ffedc4970e35cca124129ae0c78b12dcabf9bc7636e4f97b8fecf5e6f58c8c09c98ebfe7341a7cd7c4b29ed094ca506bb533284b9fd4a54738918a57593cee8b11d5a26bf970289991ac86cec9b40a4cdebb39984211c9c25bb2d8c38d18fe91b458e0d45fc5dfb54b2e0eb2759afe6dee5f2722ac9f75e41e17b266824bf8d5daa)

### ⚙ Dependencies

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

* `AWS_ACCESS_KEY_ID`
  
* `AWS_SECRET_ACCESS_KEY`
  
* `AWS_REGION`
  
* `AWS_LAMBDA_ROLE_ARN`

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

### 📌 How this project was build

#### 1. Data Versioning

**Upload the dataset file in a S3 Bucket**

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

**Configure data versioning - [DVC](https://dvc.org/)**

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

#### 2. Sagemaker (Exploratory Analysis)

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

#### 3. Configure CI-CD (Github workflows)

#### 4. Documentation

#### 5. Logging

#### 6. Monitoring

### 📌 How to use this project

Make sure your data folder is up to date with dvc:
```bash
 $ dvc status
 $ dvc pull
```

To run the scripts separately:
```bash
 # Root folder 
 $ python -m src.preprocess
 $ python -m src.train
```

Run tests:
```bash
 # Root folder
 $  pytest
```

<div align="center">
    <br>
    @2024, Insper. 9° Semester, Computer Engineering.<br>
    Machine Learning Ops & Interviews Discipline
</div>
