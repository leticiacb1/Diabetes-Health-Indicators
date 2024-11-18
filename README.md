## 🏥 Diabetes Health Indicators

**Diabetes** is among the most prevalent chronic diseases in the United States, impacting millions of Americans each year and exerting a significant financial burden on the economy. 
**Diabetes** is a serious chronic disease in which individuals lose the ability to effectively regulate levels of glucose in the blood, and can lead to reduced quality of life and life expectancy.

* Download the dataset used in this project, [here](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/data).

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

Also create a `.env` file with the following:

```bash
    AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
    AWS_SECRET_ACCESS_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaa"
    AWS_REGION="xx-xxxx-2"
    AWS_LAMBDA_ROLE_ARN="arn:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
``` 

Configure your AWS credentials:

```bash
    aws configure
```

### 📌 How to use this project



<div align="center">
    <br>
    @2024, Insper. 9° Semester, Computer Engineering.<br>
    Machine Learning Ops & Interviews Discipline
</div>
