import boto3

from config.config import Config
from src.dataclass.log_manager import LogManager
from botocore.exceptions import ClientError

class ContainerRegistry():

    def __init__(self, logger: LogManager, repository_name: str) -> None:
        self.repository_arn = None
        self.repository_uri = None
        self.repository_name = repository_name

        # Logging
        self.logger = logger

        # Load environment variables
        self.config = Config()
        self.config.load()

        # ECR Client
        self.ecr_client = boto3.client("ecr",
                                        aws_access_key_id=self.config.ACCESS_KEY,
                                        aws_secret_access_key=self.config.SECRET_KEY,
                                        region_name=self.config.REGION
                                       )

    def create_repository(self) -> None:
        '''
        Create ECR repository in AWS using the credentials in .env file

        :return: None
        '''
        try:
            try:
                response = self.ecr_client.describe_repositories(repositoryNames=[self.repository_name])
                self.logger.log.info(f"\n [INFO]  Repository '{self.repository_name}' already exists. \n ")

                self.logger.log.info(
                    f"\n [INFO] Deleting repository that already exists to create a new one ... \n")
                self.clean_up()

            except ClientError as e:
                self.logger.log.info(
                    f"\n [INFO] Repository '{self.repository_name}' does not exist. Proceeding with creation. \n")


            response = self.ecr_client.create_repository(repositoryName=self.repository_name,
                                                         imageScanningConfiguration={"scanOnPush": True},
                                                         imageTagMutability="MUTABLE",
                                                         )
            self.repository_arn = response['repository']['repositoryArn']
            self.repository_uri = response['repository']['repositoryUri']

            self.logger.log.info(f"\n [INFO] Create a ECR repository with name {self.repository_name}. \n ")
            self.logger.log.info(f"\n [INFO] > Repository Arn : {self.repository_arn}")
            self.logger.log.info(f"\n [INFO] > Repository Uri : {self.repository_uri}")

        except Exception as e:
            self.logger.log.error(f"\n [ERROR] An unexpected error occurred: {e} \n")

    def check_content(self) -> None:
        '''
        Check ECR content

        :return: None
        '''

        try:
            response = self.ecr_client.list_images(repositoryName=self.repository_name)
            images = response.get('imageIds', [])

            if not images:
                self.logger.log.info(f"\n [INFO] Repository '{self.repository_name}' is empty.\n")
            else:
                self.logger.log.info(f"\n [INFO] Repository '{self.repository_name}' contains the following images:\n")
                for image in images:
                    self.logger.log.info(f"\n [INFO]  > Image Tag: {image.get('imageTag', 'None')} | Digest: {image['imageDigest']}")

        except Exception as e:
            self.logger.log.error(f"\n [ERROR] Failed to check content ECR repository {self.repository_name}: {e} \n")

    def clean_up(self) -> None:
        '''
        Delete ECR repository

        :return: None
        '''
        try:
            # Delete the repository
            self.ecr_client.delete_repository(
                repositoryName=self.repository_name,
                force=True
            )
            self.logger.log.info(f"\n [INFO] Successfully deleted repository '{self.repository_name}'. \n")
        except ClientError as e:
            if e.response['Error']['Code'] == 'RepositoryNotFoundException':
                self.logger.log.info(f"\n [ERROR]  Repository {self.repository_name} does not exist. Nothing to delete'. \n")
            else:
                self.logger.log.error(f"\n [INFO]  Failed to create ECR repository {self.repository_name}. \n")
        except Exception as e:
            self.logger.log.error(f"\n [ERROR] An unexpected error occurred: {e} \n")