import boto3
import random
import string

from config.config import Config
from src.dataclass.log_manager import LogManager

from botocore.exceptions import ClientError

class Gateway():

    def __init__(self, logger: LogManager, api_name: str) -> None:
        self.api_id = None
        self.endpoint = None
        self.lambda_target = None

        self.api_name = api_name
        self.id_num = "".join(random.choices(string.digits, k=7))
        self.protocol_type = "HTTP"
        self.version = "1.0"

        #Logging
        self.logger = logger

        # Load environment variables
        self.config = Config()
        self.config.load()

        # API client
        self.api_gateway_client = boto3.client( "apigatewayv2",
                                         aws_access_key_id=self.config.ACCESS_KEY,
                                         aws_secret_access_key=self.config.SECRET_KEY,
                                         region_name=self.config.REGION
                                       )

    def _get_lambda_function(self, function_name: str):
        '''
        Get the lamda function associated with the function_name

        :param function_name: lambda function name
        :return: None
        '''
        lambda_client = boto3.client("lambda",
                                     aws_access_key_id=self.config.ACCESS_KEY,
                                     aws_secret_access_key=self.config.SECRET_KEY,
                                     region_name=self.config.REGION
                                     )

        lambda_function = lambda_client.get_function(FunctionName=function_name)
        self.lambda_target = lambda_function["Configuration"]["FunctionArn"]

        self.logger.log.info("\n [INFO] Get lambda function. \n")

    def _set_permissions(self, function_name: str) -> None:
        '''
        Add permissions in lambda function for gateway access

        :param function_name: lambda function name
        :return: None
        '''
        lambda_client = boto3.client( "lambda",
                                      aws_access_key_id=self.config.ACCESS_KEY,
                                      aws_secret_access_key=self.config.SECRET_KEY,
                                      region_name=self.config.REGION
                                    )

        api_gateway_permissions = lambda_client.add_permission( FunctionName=function_name,
                                                                       StatementId="api-gateway-permission-statement-" + self.id_num,
                                                                       Action="lambda:InvokeFunction",
                                                                       Principal="apigateway.amazonaws.com",
                                                                     )

        self.logger.log.info(f"\n [INFO] Set lambda function permissions for API.\n")

    def _api_exists(self, api_name: str) -> bool:
        '''
        Check if an API with the given name already exists.

        :param api_name: The name of the API to check
        :return: True if the API exists, otherwise False
        '''
        try:
            response = self.api_gateway_client.get_apis(MaxResults="5000")
            for api in response['Items']:
                if api['Name'] == api_name:
                    self.api_id = api['ApiId']
                    self.endpoint = api['ApiEndpoint']
                    self.logger.log.info(f"\n [INFO] API '{api_name}' already exists with Endpoint: {self.endpoint} \n")
                    return True
            return False
        except ClientError as e:
            self.logger.log.error(f"\n [ERROR] Failed to check if API exists: {e} \n")
            return False

    def create_api(self, function_name: str) -> None:
        '''
        Create api with name {api_name} for lambda function with name {function_name}

        :param api_name: api name
        :param function_name: lambda function name
        :return: None
        '''

        try:
            # Check if the API already exists
            if self._api_exists(self.api_name):
                self.logger.log.info(f"\n [INFO] Gateway '{self.api_name}' already exists.  \n  > Api_ID = {self.api_id} \n  > Api_Endpoint = {self.endpoint} \n")
                self.logger.log.info(f"\n [INFO] Deleting repository that already exists to create a new one ...\n")
                self.clean_up()

            self._get_lambda_function(function_name)
            self._set_permissions(function_name)

            self.logger.log.info(f"\n [INFO] Create API with name {self.api_name} \n")
            api_gateway_create = self.api_gateway_client.create_api(Name=self.api_name,
                                                                  ProtocolType=self.protocol_type,
                                                                  Version=self.version,
                                                                  RouteKey="ANY /",
                                                                  # This will create an API with a single route for all methods
                                                                  Target=self.lambda_target,
                                                                  )
            self.api_id = api_gateway_create["ApiId"]
            self.endpoint = api_gateway_create["ApiEndpoint"]
            self.logger.log.info(f"\n [INFO] Check API Endpoint : {self.endpoint} \n")
        except Exception as e:
            self.logger.log.error(f"\n [ERROR] Unexpected error: {str(e)} \n")
            raise e

    def create_route(self, HTTP_method: str, route_key: str) -> None:
        '''
        Create HTTP route in api for HTTP method

        :param HTTP_method: HTTP method
        :param route_key: api rout for HTTP method
        :return: None
        '''
        self.logger.log.info(f"\n [INFO] Create a route for API \n")
        self.logger.log.info("    > HTTP method : " + HTTP_method)
        self.logger.log.info("    > Route : " + route_key)

        # Create an integration between the API Gateway and the Lambda function
        integration_response = self.api_gateway_client.create_integration(
            ApiId=self.api_id,
            IntegrationType="AWS_PROXY",
            IntegrationMethod=HTTP_method,
            IntegrationUri=self.lambda_target,
            PayloadFormatVersion="2.0",
        )

        # Create a route for the POST method
        route_response = self.api_gateway_client.create_route(
            ApiId=self.api_id,
            RouteKey=route_key,
            Target=f"integrations/{integration_response['IntegrationId']}",
        )

    def clean_up(self) -> None:
        """
        Delete the specified API Gateway by its ID.

        :return: None
        """
        try:
            self.api_gateway_client.delete_api(ApiId=self.api_id)
            self.logger.log.info(f"\n [INFO] Successfully deleted API with ID: {self.api_id} \n")
        except Exception as e:
            self.logger.log.error(f"\n [ERROR] Failed to delete API with ID: {self.api_id}. Error: {e} \n")
            raise e
