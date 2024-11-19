# import boto3
# import os
#
# # Initialize S3 client
# s3 = boto3.client('s3')
#
# # Define the S3 path of the notebook and local path to save
# s3_bucket = 'your-bucket-name'
# s3_key = 'path/to/your/notebook.ipynb'
# local_path = './local_folder/notebook.ipynb'
#
# # Download the notebook from S3
# s3.download_file(s3_bucket, s3_key, local_path)
# print(f"Notebook downloaded to {local_path}")