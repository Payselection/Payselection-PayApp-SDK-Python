from enum import Enum


class PaymentMethod(str, Enum):
    CARD = 'Card'
    YANDEX = 'Yandex'
    EXTERNAL_FORM = 'ExternalForm'
    QR = 'QR'
    SBP = 'SBP'
    SBER_PAY = 'SberPay'
    PODELI = 'Podeli'
    ALFA_PAY = 'AlfaPay'


class Event(str, Enum):
    PAYMENT = 'Payment'
    BLOCK = 'Block'
    FAIL = 'Fail'
    REFUND = 'Refund'
    CANCEL = 'Cancel'
    THREEDS = '3DS'
    PAYOUT = 'Payout'
    REDIRECT_3DS = 'Redirect3DS'
