from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.headerregistry import Address
from string import Template
from datetime import date

from .user import User


def read_email_template(file_name):
    with open(file_name, 'r', encoding='utf-8') as templ_file:
        content = templ_file.read()
    return Template(content)

def get_message(html, sender_user, receiver_user):
    """Build the message that will be sent!"""
    dt = date.today().isoformat()
    msg = EmailMessage()
    msg['Subject'] = f"send mails to stmp local server to camaradas authenticated - {dt}!"
    msg['From'] = Address(display_name=sender_user.cn, username=sender_user.name, domain=sender_user.host)
    msg['To'] = Address(display_name=receiver_user.cn, username=receiver_user.name, domain=receiver_user.host)

    mail = html.substitute(
            mail_date=dt,
            sender_name=sender_user.name,
            sender_mail=sender_user.mail,
            receiver_cn=receiver_user.cn,
            receiver_mail=receiver_user.mail
    )
    msg.add_alternative(mail)

    return msg

def send_mail(config, entry):
    """Should send emails by provinding server settings, user entry and a html template!"""
    # connection setup 
    ip = config['SMTP_ADDR'] 
    host = config['HOST_NAME'] 
    user = config['SMTP_USER']
    passwd = config['SMTP_AUTH_PASS']

    # user authenticated  
    sender_user = User(cn=f'{user} surname', name=user, sn='surname', mail=f"{user}@{host}", host=host)
    receiver_user = entry # user parsed from the entry of AD server
    html = read_email_template('template_mail.html')

    msg = get_message(html, sender_user, receiver_user) # html email

    # send email to smtp server
    with smtplib.SMTP(ip, port=25) as server:
        server.set_debuglevel(1)
        server.starttls()
        server.login(f'{user}@{host}', passwd)
        server.send_message(msg)
        server.quit()
    
    
    return msg
