import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('amzn-clinic1data')

def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}

    doctor = params.get("doctor")
    date = params.get("date")

    if not doctor or not date:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "doctor and date are required"})
        }

    # Query all matching appointments
    response = table.scan(
        FilterExpression="Doctor = :doc AND #d = :dt",
        ExpressionAttributeValues={
            ":doc": doctor,
            ":dt": date
        },
        ExpressionAttributeNames={
            "#d": "Date"
        }
    )

    # Safely extract time values (ensure always a **list** of strings)
    booked_times = []
    for item in response.get("Items", []):
        if "Time" in item and isinstance(item["Time"], str):
            booked_times.append(item["Time"])

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"booked": booked_times})   # ✅ Always array
    }
