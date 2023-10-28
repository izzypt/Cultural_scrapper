import re
import os
import ssl
import smtplib
import subprocess
from os.path import basename
from email.message import EmailMessage

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"

def start_scripts(email):
    print(f"We will start scraping and send email to {email}!!!")
    try:
        process = subprocess.Popen(["python3", "agenda_lx.py"])
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script agendalx.py: {e}")
        return False
    return True

def is_valid_email(email):
    return re.match(email_pattern, email) is not None

def send_email():
    EMAIL_TITLE = 'Relatório de Eventos Culturais'
    BODY = 'Olá, Envio em anexo o relatório com os eventos culturais de Lisboa, Sintra, Cascais e Torres Vedras.'
    em = EmailMessage()
    em['From'] = os.getenv('SENDER_EMAIL')
    em['To'] = os.getenv('REC_EMAIL')
    em['Subject'] = EMAIL_TITLE
    em.set_content(BODY)

    em.add_attachment(open('agenda_cultural.csv', 'rb').read(), maintype='application', subtype='octet-stream', filename=basename('agenda_lx.csv'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(os.getenv('SENDER_EMAIL'), os.getenv('PASSWORD'))
        smtp.sendmail(os.getenv('SENDER_EMAIL'), os.getenv('REC_EMAIL'), em.as_string())
    print(f"E-mail enviado para {os.getenv('REC_EMAIL')} com as últimas novidades da agenda cultural.")