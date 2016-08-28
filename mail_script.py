# !/usr/bin/env python
#  -*- coding: utf-8 -*-

import logging
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

def email_log_in():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ['EMAIL_ADDRESS'], os.environ['EMAIL_PASSWORD'])

def mail_update(message, mail_to):
    msg = MIMEMultipart()
    msg['Subject'] = "Today's filings!"
    msg['From'] = os.environ['EMAIL_ADDRESS']
    msg['BCC'] = mail_to
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    
    server.sendmail(os.environ['EMAIL_ADDRESS'], mail_to, text)
    server.quit()