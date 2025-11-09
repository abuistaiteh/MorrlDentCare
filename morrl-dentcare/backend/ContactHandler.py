import json
import os
import uuid
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

TABLE_NAME = os.environ.get('TABLE_NAME', 'MorrlDentCare_ContactMessages')
TO_EMAIL   = os.environ.get('TO_EMAIL')
FROM_EMAIL = os.environ.get('FROM_EMAIL')

table = dynamodb.Table(TABLE_NAME)

def resp(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    # Handle CORS preflight (HTTP API may auto-handle, this is safe to keep)
    if event.get("httpMethod") == "OPTIONS":
        return resp(200, {"message": "CORS OK"})

    try:
        body = json.loads(event.get("body", "{}"))
        name    = (body.get("name") or "").strip()
        email   = (body.get("email") or "").strip()
        subject = (body.get("subject") or "").strip()
        message = (body.get("message") or "").strip()

        # Basic validation
        if not all([name, email, subject, message]):
            return resp(400, {"error": "All fields are required."})
        if "@" not in email or "." not in email:
            return resp(400, {"error": "Please enter a valid email address."})

        # Save to DynamoDB
        msg_id = str(uuid.uuid4())
        item = {
            "MessageId": msg_id,
            "Name": name,
            "Email": email,
            "Subject": subject,
            "Message": message,
            "CreatedAt": datetime.utcnow().isoformat()
        }
        table.put_item(Item=item)

        # Send Email via SES
        # NOTE: In SES Sandbox, both FROM and TO must be verified.
        email_subject = f"[Morrl DentCare] New contact message: {subject}"
        email_body = (
            f"New contact message from Morrl DentCare website\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}\n\n"
            f"MessageId: {msg_id}\n"
            f"Time (UTC): {item['CreatedAt']}\n"
        )

        ses.send_email(
            Source=FROM_EMAIL,
            Destination={"ToAddresses": [TO_EMAIL]},
            Message={
                "Subject": {"Data": email_subject, "Charset": "UTF-8"},
                "Body": {
                    "Text": {"Data": email_body, "Charset": "UTF-8"}
                }
            }
        )

        return resp(200, {"message": "Message sent successfully!"})

    except Exception as e:
        return resp(500, {"error": str(e)})
