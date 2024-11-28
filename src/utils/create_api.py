from ..dataclass.gateway import Gateway
from ..dataclass.log_manager import LogManager

# Variaveis
api_name =  "mlops-project-diabetes-gateway"
function_name =  "mlops-project-diabetes-lambda-function"
logger = LogManager(logger_name = "gateway_logger")

# Create gateway
gateway = Gateway(logger, api_name)
gateway.create_api(function_name)
gateway.create_route(HTTP_method="POST", route_key="POST /predict")