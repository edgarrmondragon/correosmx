import json
import os

import boto3
import jinja2
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from correos import get_validation_info, get_tracking_data
from templates import render_tracking

client = boto3.client('sns')
env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))

def send_status(event, context):

    with requests.session() as session:
        session.headers['user-agent'] = 'Mozilla/5.0'

        validation = get_validation_info(session)
        data = get_tracking_data(
            session,
            validation,
            os.getenv('GUIA'),
            os.getenv('PERIODO', 2020),
        )

    message = Mail(
        from_email=os.getenv('EMAIL_FROM'),
        to_emails=os.getenv('EMAIL_TO'),
        subject='Seguimiento de envío',
        html_content=render_tracking(data, env),
    )

    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    response = sg.send(message)

    return {
        'statusCode': response.status_code,
        'body': response.body.decode(),
        'headers': dict(response.headers),
    }
