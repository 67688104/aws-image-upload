
import json
import boto3
import base64
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "image-upload-demo-2026"

def lambda_handler(event, context):

    try:
        body = json.loads(event["body"])

        image_data = body["image"]
        file_name = body["fileName"]

        # Remove base64 header if present
        if "," in image_data:
            image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        key = "uploads/" + str(uuid.uuid4()) + "-" + file_name

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=image_bytes,
            ContentType=body.get("contentType", "image/jpeg")
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Image uploaded successfully via GitHub Actions! ",
                "fileName": file_name,
                "s3Key": key
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
