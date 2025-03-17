import re
from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated

from payselection.core.enums import PaymentType
from payselection.core.enums import TypeLink
from payselection.core.utils.currency_code import ISO4217

AMOUNT = Annotated[
    str,
    Field(
        alias='Amount',
        min_length=1,
        max_length=16,
        pattern=r'^\d+(?:\.\d{2})?$',
    ),
]

DATE_MAPPING = {
    'day': 1,
    'week': 7,
    'month': 30,
}


class MerchantConfiguration(BaseModel):
    site_id: int
    secret_key: str
    public_key: str
    merchant_url_address: HttpUrl


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class RequestIdSchema(BaseSchema):
    request_id: Annotated[str, Field(exclude=True)]


class PhonesSchema(BaseModel):
    phones: Annotated[Optional[List[str]], Field(default=None)]

    @field_validator('phones', mode='before')
    @classmethod
    def validate_phones(cls, values: [Optional[List[str]]]):
        if values is None:
            return None
        pattern = re.compile(r'^(\d{1,17}|\+\d{1,18})$')
        for phone in values:
            if not pattern.match(phone):
                raise ValueError(f'Invalid phone number: {phone}')
        return values


class CustomerInfo(BaseSchema):
    is_podeli: Annotated[
        Optional[bool],
        Field(
            default=False,
            exclude=True,
        ),
    ]
    mcc: Annotated[Optional[int], Field(None, exclude=True)]
    email: Annotated[Optional[EmailStr], Field(None, alias='Email')]
    receipt_email: Annotated[
        Optional[EmailStr],
        Field(None, alias='ReceiptEmail'),
    ]
    phone: Annotated[Optional[str], Field(None, alias='Phone')]
    language: Annotated[
        Optional[str],
        Field(
            None,
            alias='Language',
            min_length=2,
            max_length=2,
            pattern=r'^[A-Za-z]+$',
        ),
    ]
    address: Annotated[
        Optional[str],
        Field(
            None,
            alias='Address',
            min_length=1,
            max_length=100,
        ),
    ]
    town: Annotated[
        Optional[str],
        Field(
            None,
            alias='Town',
            min_length=1,
            max_length=100,
        ),
    ]
    zip: Annotated[
        Optional[str],
        Field(None, alias='ZIP', min_length=1, max_length=20),
    ]
    country: Annotated[
        Optional[str],
        Field(
            None,
            alias='Country',
            min_length=3,
            max_length=3,
            pattern=r'^[A-Z]{3}$',
        ),
    ]
    user_id: Annotated[Optional[str], Field(None, alias='UserId')]
    first_name: Annotated[Optional[str], Field(None, alias='FirstName')]
    last_name: Annotated[Optional[str], Field(None, alias='LastName')]
    date_of_birth: Annotated[Optional[str], Field(None, alias='DateOfBirth')]

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            pattern = r'^\+7\d{10}$'
            if not re.match(pattern, value):
                raise ValueError(
                    'The phone number must be in '
                    'the international format +79999999999 without spaces.',
                )
        return value

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, value):
        try:
            date_of_birth = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(
                'Invalid date format or non-existent date (YYYY-MM-DD)',
            )

        if date_of_birth > date.today():
            raise ValueError('Date of birth cannot be in the future')

        return value

    @field_validator('phone', mode='after')
    @classmethod
    def validate_phone_for_podeli(
        cls,
        value: Optional[str],
        values,
    ) -> Optional[str]:
        if values.data.get('mcc') == 4814 and value is None:
            raise ValueError('The field is required for MCC 4814')
        return value

    @field_validator('is_podeli', mode='after')
    @classmethod
    def validate_is_podeli(cls, value, values):
        if value and any(
            [
                values.data.get('email') is None,
                values.data.get('phone') is None,
                values.data.get('first_name') is None,
                values.data.get('last_name') is None,
                values.data.get('date_of_birth') is None,
            ],
        ):
            missing_fields = [
                field
                for field in [
                    'email',
                    'phone',
                    'first_name',
                    'last_name',
                    'date_of_birth',
                ]
                if values.data.get(field) is None
            ]
            raise ValueError(
                f'The following fields are required for '
                f"'podeli' method: {', '.join(missing_fields)}",
            )
        return value


class MetaDataBase(BaseSchema):
    payment_type: Annotated[
        Optional[PaymentType],
        Field(None, alias='PaymentType'),
    ]
    type_link: Annotated[Optional[TypeLink], Field(None, alias='TypeLink')]
    preview_form: Annotated[Optional[bool], Field(None, alias='PreviewForm')]
    send_sms: Annotated[Optional[bool], Field(None, alias='SendSMS')]


class ExtraDataBase(BaseSchema):
    class ShortDescription(BaseSchema):
        ru: Annotated[Optional[str], Field(None, max_length=50)]
        en: Annotated[Optional[str], Field(None, max_length=50)]

    return_url: Annotated[Optional[HttpUrl], Field(None, alias='ReturnUrl')]
    success_url: Annotated[Optional[HttpUrl], Field(None, alias='SuccessUrl')]
    decline_url: Annotated[Optional[HttpUrl], Field(None, alias='DeclineUrl')]
    webhook_url: Annotated[Optional[HttpUrl], Field(None, alias='WebhookUrl')]
    short_description: Annotated[
        Optional[ShortDescription],
        Field(
            None,
            alias='ShortDescription',
        ),
    ]


class SplitData(BaseSchema):
    submerchant_id: Annotated[
        str,
        Field(
            alias='SubmerchantId',
            min_length=1,
            max_length=100,
        ),
    ]
    amount: AMOUNT
    description: Annotated[
        Optional[str],
        Field(
            None,
            alias='Description',
            min_length=1,
            max_length=99,
        ),
    ]


class OrderIdSchema(BaseSchema):
    order_id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            alias='OrderId',
            pattern=r'^[\x20-\x7E№ığüşöçİĞÜŞÖÇ]{1,100}$',
        ),
    ]


class TransactionIdSchema(BaseSchema):
    transaction_id: Annotated[
        str,
        Field(
            alias='TransactionId',
            min_length=16,
            max_length=16,
        ),
    ]


class PayBase(TransactionIdSchema):
    amount: AMOUNT
    currency: Annotated[ISO4217, Field(alias='Currency')]


class PaymentRequestBase(OrderIdSchema, BaseSchema):
    amount: AMOUNT
    currency: Annotated[ISO4217, Field(alias='Currency')]
    description: Annotated[
        str,
        Field(alias='Description', min_length=1, max_length=250),
    ]
    rebill_flag: Annotated[Optional[bool], Field(None, alias='RebillFlag')]
