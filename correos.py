from typing import Mapping, Dict, List

from bs4 import BeautifulSoup
from requests import Session

URL = 'https://www.correosdemexico.gob.mx/SSLServicios/SeguimientoEnvio/Seguimiento.aspx'


def get_validation_info(s: Session) -> Dict[str, str]:
    r = s.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')

    return {
        tag['name']: tag['value'] 
        for tag in soup.select('input[name^=__]')
    }


def get_tracking_data(
        s: Session,
        validation: Mapping[str, str],
        tracking_id: str,
        period: str,
    ) -> List[Dict[str, str]]:

    request_data = {
        **validation,
        '__EVENTTARGET': 'Busqueda',
        'Guia': tracking_id,
        'Periodo': period,
    }
    
    r = s.post(URL, data=request_data)
    soup = BeautifulSoup(r.content, 'lxml')

    data = []

    # Header
    header = [th.text for th in soup.select('#GDDatos th')]

    # Rows
    for tr in soup.select('#GDDatos tr'):
        rows = tr.select('td')
        if rows:
            data.append(dict(zip(header, [td.text for td in rows])))

    return data


if __name__ == '__main__':
    import json
    import os

    import requests
    from jinja2 import Environment, FileSystemLoader
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    from templates import render_tracking

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    GUIA = os.getenv('GUIA')
    PERIODO = os.getenv('PERIODO', 2020)
    env = Environment(loader=FileSystemLoader('./templates'))
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'
        validation = get_validation_info(s)
        data = get_tracking_data(s, validation, GUIA, PERIODO)

    message = Mail(
        from_email=os.getenv('EMAIL_FROM'),
        to_emails=os.getenv('EMAIL_TO'),
        subject='Seguimiento de envío',
        html_content=render_tracking(data, env),
    )

    response = sg.send(message)

    status_code = response.status_code
    body = response.body.decode()
    headers = dict(response.headers)

    print(status_code, type(status_code))
    print(body, type(body))
    print(headers, type(headers))
