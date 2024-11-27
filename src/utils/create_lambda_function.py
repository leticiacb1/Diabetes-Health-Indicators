from ..dataclass.lambda_function import LambdaFunction
from ..dataclass.log_manager import LogManager

# Variaveis
function_name =  "mlops-project-diabetes-lambda-function"
image_uri = "820926566402.dkr.ecr.us-east-2.amazonaws.com/mlops-project-diabetes-ecr:latest" # <repositoryUri>:<imageTag>
logger = LogManager(logger_name = "lambda_function_logger")

# Create Lambda Function
lambda_function = LambdaFunction(logger, function_name)
lambda_function.create_function_from_image(image_uri)