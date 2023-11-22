from enum import Enum

class MailingConstants(Enum):
    SENDER_EMAIL = 'secure-admin@indicatortester.com'
    RECEIVER_EMAIL = 'mustafaitju@gmail.com'

    CANDLES_REPORT_EMAIL_SUBJECT = '[IndicatorTester] Candles Fetcher Report'

    SMTP_USER = 'AKIAR4LX2SAMBNX67IWY'
    SMTP_PASSWORD = 'BAiLmIj4JB+av+g4Ry81CsBnwc3dPpIdtVksyu2BTYFQ'
    SMTP_SERVER = 'email-smtp.eu-west-1.amazonaws.com'
    SMTP_PORT = 2587