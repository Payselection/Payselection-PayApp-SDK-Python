from pydantic import Field
from pydantic import field_validator
from typing_extensions import Annotated

from payselection.core.schemas.schema import BaseSchema
from payselection.core.schemas.schema import PayBase
from payselection.gateway_payment.schemas.payout import CardSchema


class CardDataSchema(BaseSchema):
    class TransactionDetails(PayBase):
        transaction_id: Annotated[None, Field(None, exclude=True)]

    class PaymentDetails(CardSchema):
        cvc: Annotated[
            str,
            Field(
                alias='CVC',
                min_length=3,
                max_length=4,
                pattern=r'\d{3,4}',
            ),
        ]
        exp_month: Annotated[
            str,
            Field(
                alias='ExpMonth',
                pattern=r'\d{2}',
                min_length=2,
                max_length=2,
            ),
        ]
        exp_year: Annotated[
            str,
            Field(
                alias='ExpYear',
                min_length=2,
                max_length=2,
                pattern=r'\d{2}',
            ),
        ]

        @field_validator('exp_month')
        @classmethod
        def validate_exp_month(cls, value):
            if not (1 <= int(value) <= 12):
                raise ValueError('The field is not valid')
            return value

    transaction_details: Annotated[
        TransactionDetails,
        Field(alias='TransactionDetails'),
    ]
    payment_method: Annotated[
        str,
        Field(default='Card', alias='PaymentMethod'),
    ]
    payment_details: Annotated[PaymentDetails, Field(alias='PaymentDetails')]
    message_expiration: Annotated[float, Field(alias='MessageExpiration')]
