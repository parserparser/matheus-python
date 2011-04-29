from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import Encoders
from email.parser import HeaderParser
import email
import base64

import smtplib
import imaplib
import os
import re
import StringIO

from_ = 'SportsParser@gmail.com'
server = 'smtp.gmail.com:587'
use_tls = True
password = 'w5Zm4r1Vqr9088'

def sendemail(dest, subj, body):
    msg = MIMEMultipart()

    msg['From'] = from_
    msg['To'] = dest
    msg['Subject'] = subj

    msg.attach(MIMEText(body))

    hostport = server.split(':')
    mailserver = smtplib.SMTP(hostport[0], int(hostport[1]))
    if use_tls:
        mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(from_, password)
    mailserver.sendmail(from_, dest, msg.as_string())
    mailserver.close()
