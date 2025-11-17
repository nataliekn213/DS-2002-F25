import boto3

# create client
s3 = boto3.client('s3', region_name="us-east-1")

# vars needed
bucket_name = "ds2002-f25-gzg8pf"
object_name = "team_lillian_public.jpg"
expires_in = 300

response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_name},
    ExpiresIn=expires_in
)

print("Presigned URL:", response)