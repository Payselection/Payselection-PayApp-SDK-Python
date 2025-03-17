from ipaddress import ip_address
from typing import Optional
from typing import Union

from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from pydantic_extra_types.payment import PaymentCardNumber
from typing_extensions import Annotated

from payselection.core.schemas.receipt.receipt_data import ReceiptData
from payselection.core.schemas.schema import BaseSchema
from payselection.core.schemas.schema import PaymentRequestBase
from payselection.core.schemas.schema import RequestIdSchema
from payselection.gateway_payment.enums import PayoutMethod
from payselection.web_payment.schema import (
    CustomerInfo as CustomerInfoBase,
)

CARD_HOLDER_PATTERN = r'^[a-zA-Z.,-]+\s[a-zA-Z.,-]+(?:\s[a-zA-Z.,-]+){0,2}$'
TOKEN_VALUE_PATTERN = (
    r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]'
    r'{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$'
)


class CardSchema(BaseSchema):
    card_number: Annotated[PaymentCardNumber, Field(alias='CardNumber')]
    cardholder_name: Annotated[
        str,
        Field(
            alias='CardholderName',
            min_length=3,
            max_length=30,
            pattern=CARD_HOLDER_PATTERN,
        ),
    ]


class TokenSchema(BaseSchema):
    payout_token: Annotated[
        str,
        Field(
            alias='PayoutToken',
            min_length=36,
            max_length=36,
            pattern=TOKEN_VALUE_PATTERN,
        ),
    ]


class SBPSchema(BaseSchema):
    phone_number: Annotated[
        str,
        Field(alias='PhoneNumber', pattern=r'^[+]\d{2,}$'),
    ]
    bank_code: Annotated[str, Field(alias='BankCode', min_length=1)]


class PayoutSchema(PaymentRequestBase, RequestIdSchema):
    class CustomerInfo(CustomerInfoBase):
        receipt_email: Annotated[Optional[str], Field(None, exclude=True)]
        user_id: Annotated[Optional[str], Field(None, exclude=True)]
        ip: Annotated[Optional[str], Field(None, alias='IP')]

        @field_validator('ip')
        @classmethod
        def validate_ip(cls, value: str) -> str:
            ip_address(value)
            return value

    class ExtraData(BaseSchema):
        webhook_url: Annotated[
            Optional[HttpUrl],
            Field(None, alias='WebhookUrl'),
        ]

    rebill_flag: Annotated[Optional[bool], Field(None, exclude=True)]

    customer_info: Annotated[
        Optional[CustomerInfo],
        Field(None, alias='CustomerInfo'),
    ]
    extra_data: Annotated[Optional[ExtraData], Field(None, alias='ExtraData')]
    payout_method: Annotated[PayoutMethod, Field(alias='PayoutMethod')]
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    payout_details: Annotated[
        Union[CardSchema, TokenSchema, SBPSchema],
        Field(
            alias='PayoutDetails',
        ),
    ]

    @field_validator('payout_details')
    @classmethod
    def validate_payment_details(cls, value, values):
        method = values.data.get('payout_method')
        method_to_details = {
            PayoutMethod.SBP: SBPSchema,
            PayoutMethod.TOKEN: TokenSchema,
            PayoutMethod.CARD: CardSchema,
        }

        expected_model = method_to_details[method]
        if not isinstance(value, expected_model):
            raise ValueError('The field does not match the expected model')
        return value
