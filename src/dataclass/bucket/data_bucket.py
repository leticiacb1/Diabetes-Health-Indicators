from .bucket import Bucket

from src.dataclass.log_manager import LogManager

class DataBucket(Bucket):
    def __init__(self, logger: LogManager, bucket_name: str):
        Bucket.__init__(self, logger, bucket_name)

    def upload_file(self, file_path: str) -> None:
        '''
        Upload a file on a S3 Bucket
        :param file_path: string of the file path for upload
        :return: None
        '''

        key = file_path.split("/")[-1]
        self.s3_client.upload_file(file_path, self.bucket_name, key)

        self.logger.log.info(f" [INFO] The file {key} has been uploaded to the bucket {self.bucket_name}. \n")