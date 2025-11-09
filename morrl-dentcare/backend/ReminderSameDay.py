import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr

TABLE_NAME = "amzn-clinic1data"
FROM_EMAIL = "no-reply@morrl.com"
CLINIC_NAME = "Morrl DentCare"
CLINIC_PHONE = "+1 (571) 502-7375"

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    items = table.scan(FilterExpression=Attr('Date').eq(today))['Items']

    for a in items:
        send_email(a['Email'], a['Name'], a['Doctor'], a['Service'], a['Date'], a['Time'])

def send_email(to, name, doctor, service, date, time):
    subject = f"Reminder: Appointment Today – {CLINIC_NAME}"
    html = f"""
    <html><body style="font-family: Arial;">
    <p>Hi {name}, just a reminder — your appointment is today.</p>
    <p><b>{service}</b> with <b>{doctor}</b><br>
    <b>{date}</b> at <b>{time}</b></p>
    <p>If anything changes, please call <b>{CLINIC_PHONE}</b>.</p>
    <p style="color:#777;font-size:12px;">This email is sent from a no-reply address.</p>
    </body></html>
    """
    ses.send_email(Source=FROM_EMAIL,
        Destination={'ToAddresses':[to]},
        Message={'Subject':{'Data':subject}, 'Body':{'Html':{'Data':html}}})
