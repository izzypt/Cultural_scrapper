import re
import os
import ssl
import smtplib
import subprocess
from os.path import basename
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

####################
# LOAD ENVIRONMENT #
####################
dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

#################
# EMAIL PATTERN #
#################
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"

meses_em_ingles = {
    "January" : "Janeiro",
    "February" : "Fevereiro",
    "March" : "Março",
    "April" : "Abril",
    "May" : "Maio",
    "June" : "Junho",
    "July" : "Julho",
    "August" : "Agosto",
    "September" : "Setembro",
    "October" : "Outubro",
    "November" : "Novembro",
    "December" : "Dezembro"
}

##################
# UTIL FUNCTIONS #
##################
def start_scripts(email):
    print(f"We will start scraping and send email to {email}!!!")
    try:
        process = subprocess.Popen(["python3", "agenda_lx.py"])
        process.wait()
        process2 = subprocess.Popen(["scrapy", "runspider", "--nolog", "agenda_torres.py"])
        process2.wait()
        process3 = subprocess.Popen(["scrapy", "runspider", "--nolog", "agenda_sintra.py"])
        process3.wait()
        process4 = subprocess.Popen(["scrapy", "runspider", "--nolog", "agenda_cascais.py"])
        process4.wait()
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script: {e}")
        return Exception("Something went wrong when running the scraping scripts...")
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

    em.add_attachment(open(output_file(), 'rb').read(), maintype='application', subtype='octet-stream', filename=basename(output_file()))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(os.getenv('SENDER_EMAIL'), os.getenv('PASSWORD'))
        smtp.sendmail(os.getenv('SENDER_EMAIL'), os.getenv('REC_EMAIL'), em.as_string())
    print(f"E-mail enviado para {os.getenv('REC_EMAIL')} com as últimas novidades da agenda cultural.")

def mes_EN_to_PT(str):
    str_split = str.split(' ')
    mes_en = None
    mes_pt = None 
    if (len(str_split) < 3):
        return str
    for word in str_split:
        for mes in meses_em_ingles:
            if word == mes:
                mes_en = word
                mes_pt = meses_em_ingles[mes]
    str = str.replace(mes_en, mes_pt) if mes_en and mes_pt else str
    return str

def add_current_year(input_str):
    current_year = str(datetime.now().year)
    last_year = str(datetime.now().year - 1)
    next_year = str(datetime.now().year + 1)

    if (input_str.find(current_year) == -1 and input_str.find(last_year) == -1 and input_str.find(next_year) == -1) and input_str != 'N/A':
        input_str += " " + current_year

    return input_str

def add_month_and_year(data_inicial, data_final):
    if (len(data_inicial.strip().split(' ')) == 1):
        mes = data_final.split(' ')[2]
        ano = data_final.split(' ')[3]
        return data_inicial + " " + mes + " " + ano
    return data_inicial

def output_file():
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)
    return f'agenda_cultural_{day}_{month}_{year}.csv'
