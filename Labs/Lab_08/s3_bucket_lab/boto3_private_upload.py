import boto3

# create client
s3 = boto3.client('s3', region_name="us-east-1")

bucket = "ds2002-f25-gzg8pf"
local_file_path = "team_lillian.jpg"
s3_key = "team_lillian_private.jpg"

s3.upload_file(
    Filename=local_file_path,  # The local file path on your system
    Bucket=bucket,             # The S3 bucket name
    Key=s3_key                 # The destination object key in S3
)

print("Uploaded", local_file_path, "to bucket", bucket, "as", s3_key)