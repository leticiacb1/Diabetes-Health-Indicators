from ..dataclass.container import ContainerRegistry
from ..dataclass.log_manager import LogManager

# Variaveis
repository_name =  "mlops-project-diabetes-ecr"
logger = LogManager(logger_name = "ecr_logger")

# Create ECR
ecr = ContainerRegistry(logger, repository_name)
ecr.create_repository()

repository_uri = ecr.repository_uri # Value used for upload docker image

# Check repository
ecr.check_content()