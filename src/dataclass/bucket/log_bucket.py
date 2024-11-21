from .bucket import Bucket

class LogBucket(Bucket):
    def __init__(self, bucket_name: str):
        Bucket.__init__(self, bucket_name)

    def write_logs(self, msm: str, key: str) -> None:
        '''
         Save log inside a S3 Bucket.
        :param msm: Message that will be saved
        :param key: Name of the location where the message will be saved
        :return: None
        '''

        self.s3_client.put_object(Body=msm, Bucket=self.bucket_name, Key=key)

    def read_logs(self, key: str):

        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
        file_content = obj["Body"].read().decode("utf-8")

        print(f"\n [INFO] Logs stored in bucket = {self.bucket_name} and key = {key}: \n")
        print(f"\n{file_content} \n")