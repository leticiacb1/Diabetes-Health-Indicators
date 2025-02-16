import json
import boto3
import io

from config.config import Config
from src.dataclass.log_manager import LogManager
from botocore.exceptions import ClientError

class LambdaFunction():

    def __init__(self, logger: LogManager, function_name: str) -> None:
        self.function_name = function_name
        self.runtime = "python3.12"
        self.timeout = 30
        self.mem_size = 128

        # Logging
        self.logger = logger

        # Load environment variables
        self.config = Config()
        self.config.load()

        # Lambda client
        self.lambda_client = boto3.client("lambda",
                                         aws_access_key_id=self.config.ACCESS_KEY,
                                         aws_secret_access_key=self.config.SECRET_KEY,
                                         region_name=self.config.REGION
                                         )

    def create_function_from_image(self, image_uri: str) -> None:
        '''
        Create Lambda Function in AWS using the credentials in .env file

        :return: None
        '''
        try:
            # Check if the Lambda function exists
            try:
                existing_function = self.lambda_client.get_function(FunctionName=self.function_name)
                self.logger.log.info(
                    f"\n [INFO] Lambda function '{self.function_name}' already exists. \n")
                self.logger.log.info(
                    f"\n [INFO] Deleting a lambda function that already exists to create a new one ... \n")
                self.clean_up()

            except ClientError as e:
                self.logger.log.info(f"\n [INFO] Lambda function '{self.function_name}' does not exist. Proceeding with creation. \n")

            # Create the Lambda function
            lambda_response = self.lambda_client.create_function(
                FunctionName=self.function_name,
                PackageType="Image",
                Code={"ImageUri": image_uri},
                Role=self.config.ROLE_ARN,
                Timeout=self.timeout,
                MemorySize=self.mem_size,
            )
            self.logger.log.info(f"\n [INFO] Created Lambda function '{self.function_name}' successfully. \n")
            self.logger.log.info(f"  > Function ARN: {lambda_response['FunctionArn']} \n")

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            self.logger.log.error(
                f"\n [ERROR] AWS error while creating Lambda function '{self.function_name}': {error_message} \n")
            raise e
        except Exception as e:
            self.logger.log.error(f"\n [ERROR] Unexpected error: {str(e)} \n")
            raise e

    def check_content(self, input_data: dict) -> None:
        '''
        Invoke lambda function with an input.

        :param input_data: lambda function input
        :return: None
        '''
        try:
            response = self.lambda_client.invoke( FunctionName=self.function_name,
                                                      InvocationType="RequestResponse",
                                                      Payload=json.dumps(input_data)
                                                    )
                                                
            payload = response["Payload"]
            txt = io.BytesIO(payload.read()).read().decode("utf-8")

            self.logger.log.info(f"\n [INFO] Invoke Function {self.function_name}(input = {input_data}) \n")
            self.logger.log.info(f"  > Response : {txt} \n")
        except Exception as e:
            self.logger.log.error(f"\n [ERROR] Failed to call Lambda function repository {self.function_name}: {e} \n")


    def clean_up(self) -> None:
        '''
        Delete Lambda Function

        :return: None
        '''
        try:
            self.lambda_client.delete_function(FunctionName=self.function_name)
            self.logger.log.info(f"\n [INFO] Lambda function {self.function_name} deleted successfully. \n")
        except Exception as e:
            self.logger.log.error(f"\n [ERROR] An unexpected error occurred: {e} \n")