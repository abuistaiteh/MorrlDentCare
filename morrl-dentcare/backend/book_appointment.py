import json
import boto3
import uuid
from datetime import datetime, date
from boto3.dynamodb.conditions import Attr

# Hard-coded configuration
TABLE_NAME = "amzn-clinic1data"
FROM_EMAIL = "no-reply@morrl.com"   # Verified SES Email
CLINIC_NAME = "Morrl DentCare"
CLINIC_PHONE = "+1 (571) 502-7375"

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))

    name = body.get('name')
    email = body.get('email')
    doctor = body.get('doctor')
    service = body.get('service')
    appointment_date = body.get('date')
    appointment_time = body.get('time')

    # Required fields check
    if not all([name, email, doctor, service, appointment_date, appointment_time]):
        return send(400, {"error": "Missing required fields"})

    # Validate date
    try:
        appt_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    except:
        return send(400, {"error": "Invalid date"})

    if appt_date < date.today():
        return send(400, {"error": "Cannot book past dates"})

    # Prevent double booking
    existing = table.scan(
        FilterExpression=Attr('Doctor').eq(doctor) &
                         Attr('Date').eq(appointment_date) &
                         Attr('Time').eq(appointment_time)
    )
    if existing['Count'] > 0:
        return send(400, {"error": "This time is already booked."})

    # Store appointment
    appointment_id = str(uuid.uuid4())
    table.put_item(Item={
        "AppointmentsId": appointment_id,
        "Name": name,
        "Email": email,
        "Doctor": doctor,
        "Service": service,
        "Date": appointment_date,
        "Time": appointment_time
    })

    # Send confirmation email
    send_confirmation_email(email, name, doctor, service, appointment_date, appointment_time)

    return send(200, {"message": "Appointment booked!", "id": appointment_id})

def send_confirmation_email(to_email, name, doctor, service, date, time):
    subject = f"Appointment Confirmed – {CLINIC_NAME}"
    html_body = f"""
    <html><body style="font-family: Arial;">
    <h2>{CLINIC_NAME}</h2>
    <p>Hello {name}, your appointment is confirmed.</p>
    <p><b>Doctor:</b> {doctor}<br>
    <b>Service:</b> {service}<br>
    <b>Date:</b> {date}<br>
    <b>Time:</b> {time}</p>
    <p>If you need to change or cancel your appointment, please call:<br>
    <b>{CLINIC_PHONE}</b></p>
    <p style="color:#777;font-size:12px;">This email is sent from a no-reply address.</p>
    </body></html>
    """
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [to_email]},
        Message={'Subject': {'Data': subject}, 'Body': {'Html': {'Data': html_body}}}
    )

def send(code, message):
    return {
        "statusCode": code,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(message)
    }
