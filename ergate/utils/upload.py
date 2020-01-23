import os

import boto3


def upload_file(file_path, key, bucket_name):
    session = boto3.Session()
    client = session.client(
        "s3",
        region_name=os.getenv("DIGITAL_OCEAN_REGION"),
        endpoint_url="https://{}.digitaloceanspaces.com".format(
            os.getenv("DIGITAL_OCEAN_REGION")
        ),
        aws_access_key_id=os.getenv("DIGITAL_OCEAN_STORAGE_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("DIGITAL_OCEAN_STORAGE_SECRET_ACCESS_KEY"),
    )

    client.upload_file(file_path, bucket_name, key)
    client.put_object_acl(ACL="public-read", Bucket=bucket_name, Key=key)

