# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import logging
import os
import smtplib

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from jinja2 import Template, Environment, FileSystemLoader

jinja_environment = Environment(autoescape=True,loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


def email_log_in():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ['EMAIL_ADDRESS'], os.environ['EMAIL_PASSWORD'])
    return server


def mail_update(server, data, mail_to):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "Today's filings!"
        msg['From'] = os.environ['EMAIL_ADDRESS']
        msg['BCC'] = mail_to
        template = jinja_environment.get_template('working_filings.html')
        text = template.render(data)
        msg.attach(MIMEText(text, 'html'))
        text = msg.as_string()
        server.sendmail(os.environ['EMAIL_ADDRESS'], mail_to, text)
        server.quit()
    except:
        logging.warning('Mail failure')
        mail_update('ERROR FOR {0}'.format(mail_to), os.environ['ADMIN_EMAIL'])
        exit()
