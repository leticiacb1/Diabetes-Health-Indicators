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

1. Data Versioning

**Upload the dataset file in a S3 Bucket**

```bash
   # With .csv inside data folder
   # Root folder
   $ python -m src.utils.upload_data
   # After that delete .csv in data folder
```

After this the URL of the file upload is : `https://<bucket-name>.s3.<region>.amazonaws.com/<key>`

> Data URL =  https://mlops-project-diabetes-data-bucket.s3.us-east-2.amazonaws.com/diabetes_binary_health_indicators_BRFSS2015.csv

**Configure data versioning - (DVC)[https://dvc.org/]**

```bash
 $ dvc init
 $ dvc get-url <data-bucket-url> data/diabetes_data.csv
 $ dvc add data/diabetes_data.csv
```

Create a dvc bucket:

```bash
 $ python -m src.utils.dvc_bucket
```

Add S3 in dvc:

```bash
  $ dvc remote add myremote s3://<dvc-bucket-name>
  $ dvc remote default myremote
  $ dvc push
```


### 📌 How to use this project



<div align="center">
    <br>
    @2024, Insper. 9° Semester, Computer Engineering.<br>
    Machine Learning Ops & Interviews Discipline
</div>
