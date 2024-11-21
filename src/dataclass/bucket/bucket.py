import boto3

from config.config import Config
from botocore.exceptions import ClientError

class Bucket():

    def __init__(self, bucket_name: str) -> None:
        self.s3_client = None
        self.bucket_name = bucket_name

        # Load environment variables
        self.config = Config()
        self.config.load()

        # S3 Client
        self.s3_client = boto3.client("s3",
                                      aws_access_key_id=self.config.ACCESS_KEY,
                                      aws_secret_access_key=self.config.SECRET_KEY,
                                      region_name=self.config.REGION
                                      )

    def create(self) -> None:
        '''
        Create a S3 bucket in AWS using the credentials in .env file
        :return: None
        '''

        try:
            self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.config.REGION},
            )
            print("\n [INFO] Create a S3 Bucket successfully. \n")

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "BucketAlreadyOwnedByYou":
                print("\n [INFO] Bucket already exists and is owned by you. Skipping creation.\n")
            elif error_code == "BucketAlreadyExists":
                print("\n [INFO] Bucket name already taken by someone else. Skipping creation.\n")
            else:
                print(f"\n [ERROR] Failed to create bucket: {e}\n")
        except Exception as e:
            print(f"\n [ERROR] An unexpected error occurred: {e}\n")

    def check_content(self) -> None:
        '''
        Read bucket content files
        :return:
        '''
        print(f"\n [INFO] Read S3 Bucket {self.bucket_name} content. \n")

        # Store contents of bucket
        objects_list = self.s3_client.list_objects_v2(Bucket=self.bucket_name).get("Contents")

        # Iterate over every object in bucket
        for obj in objects_list:

            obj_name = obj["Key"]
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj_name)

            # Read the object’s content as text
            object_content = response["Body"].read().decode("utf-8")
            print(f" Contents of {obj_name}\n --------------")
            print(object_content[:100], end="\n\n")

    def clean_up(self) -> None:
        '''
        Delet bucket and all content inside
        :return: None
        '''
        try:
            paginator = self.s3_client.get_paginator('list_object_versions')
            for page in paginator.paginate(Bucket=self.bucket_name):
                if 'Versions' in page:
                    for version in page['Versions']:
                        self.s3_client.delete_object(Bucket=self.bucket_name, Key=version['Key'], VersionId=version['VersionId'])
                if 'DeleteMarkers' in page:
                    for marker in page['DeleteMarkers']:
                        self.s3_client.delete_object(Bucket=self.bucket_name, Key=marker['Key'], VersionId=marker['VersionId'])

            self.s3_client.delete_bucket(Bucket=self.bucket_name)
        except Exception as e:
            print(f"\n [INFO] Failed to delete bucket {self.bucket_name}: {e}")