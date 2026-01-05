from enum import Enum


class PaymentType(str, Enum):
    PAY = 'Pay'
    BLOCK = 'Block'


class SNO(str, Enum):
    OSN = 'osn'
    USN_INCOME = 'usn_income'
    USN_INCOME_OUTCOME = 'usn_income_outcome'
    ENVD = 'envd'
    ESN = 'esn'
    PATENT = 'patent'


class AgentType(str, Enum):
    BANK_PAYING_AGENT = 'bank_paying_agent'
    BANK_PAYING_SUBAGENT = 'bank_paying_subagent'
    PAYING_AGENT = 'paying_agent'
    PAYING_SUBAGENT = 'paying_subagent'
    ATTORNEY = 'attorney'
    COMMISSION_AGENT = 'commission_agent'
    ANOTHER = 'another'


class TypeLink(str, Enum):
    REUSABLE = 'Reusable'


class Period(str, Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


class PaymentMethod(str, Enum):
    FULL_PREPAYMENT = 'full_prepayment'
    PREPAYMENT = 'prepayment'
    ADVANCE = 'advance'
    FULL_PAYMENT = 'full_payment'
    PARTIAL_PAYMENT = 'partial_payment'
    CREDIT = 'credit'
    CREDIT_PAYMENT = 'credit_payment'


class PaymentObject(str, Enum):
    COMMODITY = 'commodity'
    EXCISE = 'excise'
    JOB = 'job'
    SERVICE = 'service'
    GAMBLING_BET = 'gambling_bet'
    GAMBLING_PRIZE = 'gambling_prize'
    LOTTERY = 'lottery'
    LOTTERY_PRIZE = 'lottery_prize'
    INTELLECTUAL_ACTIVITY = 'intellectual_activity'
    PAYMENT = 'payment'
    AGENT_COMMISSION = 'agent_commission'
    COMPOSITE = 'composite'
    AWARD = 'award'
    ANOTHER = 'another'
    PROPERTY_RIGHT = 'property_right'
    NON_OPERATING_GAIN = 'non-operating_gain'
    INSURANCE_PREMIUM = 'insurance_premium'
    SALES_TAX = 'sales_tax'
    RESORT_FEE = 'resort_fee'
    DEPOSIT = 'deposit'
    EXPENSE = 'expense'
    PENSION_INSURANCE_IP = 'pension_insurance_ip'
    PENSION_INSURANCE = 'pension_insurance'
    MEDICAL_INSURANCE_IP = 'medical_insurance_ip'
    MEDICAL_INSURANCE = 'medical_insurance'
    SOCIAL_INSURANCE = 'social_insurance'
    CASINO_PAYMENT = 'casino_payment'


class VatType(str, Enum):
    NONE = 'none'
    VAT0 = 'vat0'
    VAT10 = 'vat10'
    VAT110 = 'vat110'
    VAT18 = 'vat18'
    VAT118 = 'vat118'
    VAT20 = 'vat20'
    VAT120 = 'vat120'
    VAT22 = 'vat22'
    VAT122 = 'vat122'


class Measure(int, Enum):
    PCS = 0
    GM = 10
    KG = 11
    TN = 12
    CM = 20
    DM = 21
    M = 22
    SQ_CM = 30
    SQ_DM = 31
    SQ_M = 32
    ML = 40
    L = 41
    CBM = 42
    KW_HR = 50
    GIGACALORIE = 51
    DAY = 70
    HOUR = 71
    MINUTE = 72
    SECOND = 73
    KILOBYTE = 80
    MEGABYTE = 81
    GIGABYTE = 82
    TERABYTE = 83
    ANOTHER = 255


class PaymentObjectInt(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    SEVENTEEN = 17
    EIGHTEEN = 18
    NINETEEN = 19
    TWENTY = 20
    TWENTY_ONE = 21
    TWENTY_TWO = 22
    TWENTY_THREE = 23
    TWENTY_FOUR = 24
    TWENTY_FIVE = 25
    TWENTY_SIX = 26
    TWENTY_SEVEN = 27
    THIRTY = 30
    THIRTY_ONE = 31
    THIRTY_TWO = 32
    THIRTY_THREE = 33
