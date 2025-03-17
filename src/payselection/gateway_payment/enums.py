from enum import Enum


class Statuses(str, Enum):
    SUCCESS = 'success'
    VOIDED = 'voided'
    PREAUTHORIZED = 'preauthorized'
    PENDING = 'pending'
    DECLINED = 'declined'
    WAIT_FOR_3DS = 'wait_for_3ds'
    REDIRECT = 'redirect'


class PaymentMethod(str, Enum):
    CRYPTOGRAM = 'Cryptogram'
    TOKEN = 'Token'
    QR = 'QR'
    EXTERNAL_FORM = 'ExternalForm'
    CRYPTOGRAM_RSA = 'CryptogramRSA'
    SBER_PAY = 'SberPay'
    ALFA_PAY = 'AlfaPay'
    CARD = 'Card'


class TokenType(str, Enum):
    YANDEX = 'Yandex'
    INTERNAL = 'Internal'
    MTS = 'Mts'


class PayoutMethod(str, Enum):
    SBP = 'Sbp'
    TOKEN = 'Token'
    CARD = 'Card'
