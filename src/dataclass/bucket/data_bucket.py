from .bucket import Bucket

class DataBucket(Bucket):
    def __init__(self, bucket_name: str):
        Bucket.__init__(self, bucket_name)

    def upload_file(self, file_path: str) -> None:
        '''
        Upload a file on a S3 Bucket
        :param file_path: string of the file path for upload
        :return: None
        '''

        # key = Filename
        key = file_path.split("/")[-1]
        self.s3_client.upload_file(file_path, self.bucket_name, key)

        print(f"\n    [INFO] The file {key} has been uploaded to the bucket {self.bucket_name}. \n")