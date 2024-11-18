from ..dataclass.bucket.data_bucket import DataBucket

# Variaveis
bucket_name = "mlops-project-diabetes-dvc-bucket"

# Create S3 bucket
dvc_bucket = DataBucket(bucket_name)
dvc_bucket.create()
