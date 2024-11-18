from ..dataclass.bucket.data_bucket import DataBucket

# Variaveis
bucket_name = "mlops-project-diabetes-data-bucket"
file_path = "data/diabetes_binary_health_indicators_BRFSS2015.csv"

# Create S3 bucket
data_bucket = DataBucket(bucket_name)
data_bucket.create()

# Upload file content
data_bucket.upload_file(file_path)

# Check upload file
data_bucket.check_content()