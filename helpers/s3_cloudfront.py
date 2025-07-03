import boto3
import uuid
import os
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET=os.getenv("S3_BUCKET")
S3_REGION=os.getenv("S3_REGION")
CLOUDFRONT_URL=os.getenv("CLOUDFRONT_URL")
AWS_ACCESS_KEY=os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_to_s3(file: UploadFile) -> str:
    extension = file.filename.split('.')[-1] #type: ignore
    key = f"plates/{uuid.uuid4()}.{extension}"

    s3.upload_fileobj(
        file.file,
        S3_BUCKET,
        key,
        ExtraArgs={"ContentType": file.content_type}
    )

    return f"https://{CLOUDFRONT_URL}/{key}"


