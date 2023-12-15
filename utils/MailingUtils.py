import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import constants

class MailingUtils:

    @staticmethod
    def instance():
        return mailingUtils

    def sendUltimateCalculatorReport(cls, symbolSignalsDict):
        message = MIMEMultipart()
        message['From'] = constants.MailingConstants.SENDER_EMAIL.value
        message['To'] = constants.MailingConstants.RECEIVER_EMAIL.value
        message['Subject'] = Header(constants.MailingConstants.ULTIMATE_CALCULATOR_REPORT_EMAIL_SUBJECT.value, 'utf-8')
    
        body = ''
        for symbol, signals in symbolSignalsDict.items():
            body += f"<br>Crypto <b>{symbol}</b> Signals: {signals}<br>"

        message.attach(MIMEText(body, 'html'))

        stmpServer = cls._createSmtpServer()
        stmpServer.sendmail(
            constants.MailingConstants.SENDER_EMAIL.value, 
            constants.MailingConstants.RECEIVER_EMAIL.value, 
            message.as_string()
        )

    def _createSmtpServer(cls):
        server = smtplib.SMTP(constants.MailingConstants.SMTP_SERVER.value, constants.MailingConstants.SMTP_PORT.value)
        server.starttls()
        server.login(constants.MailingConstants.SMTP_USER.value, constants.MailingConstants.SMTP_PASSWORD.value)
        return server

mailingUtils = MailingUtils()