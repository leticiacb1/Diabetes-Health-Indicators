from ..dataclass.bucket.data_bucket import DataBucket
from ..dataclass.log_manager import LogManager

# Variaveis
bucket_name = "mlops-project-diabetes-dvc-bucket"
logger = LogManager(logger_name = "create_dvc_bucket_logger")

# Create S3 bucket
dvc_bucket = DataBucket(logger, bucket_name)
dvc_bucket.create()