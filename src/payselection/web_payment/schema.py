from typing import List
from typing import Optional

from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from typing_extensions import Annotated

from payselection.core.schemas.receipt.receipt_data import ReceiptData
from payselection.core.schemas.recurring import RecurringData
from payselection.core.schemas.schema import CustomerInfo
from payselection.core.schemas.schema import ExtraDataBase
from payselection.core.schemas.schema import MetaDataBase
from payselection.core.schemas.schema import PaymentRequestBase
from payselection.core.schemas.schema import RequestIdSchema
from payselection.core.schemas.schema import SplitData


class CreatePaymentSchema(RequestIdSchema):
    class PaymentRequest(PaymentRequestBase):
        extra_data: Annotated[
            Optional[ExtraDataBase],
            Field(None, alias='ExtraData'),
        ]

    metadata: Annotated[Optional[MetaDataBase], Field(None, alias='MetaData')]
    payment_request: Annotated[PaymentRequest, Field(alias='PaymentRequest')]
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    customer_info: Annotated[
        Optional[CustomerInfo],
        Field(None, alias='CustomerInfo'),
    ]
    recurring_data: Annotated[
        Optional[RecurringData],
        Field(
            None,
            alias='RecurringData',
        ),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]

    @field_validator('recurring_data')
    @classmethod
    def validate_recurring_data(cls, value, values):
        if value is None:
            return
        if not values.data['payment_request'].rebill_flag:
            raise ValueError('You must specify RebillFlag = True.')
        return value


class PaylinkSchema(CreatePaymentSchema):
    class MetaData(MetaDataBase):
        offer_url: Annotated[Optional[HttpUrl], Field(None, alias='OfferUrl')]
        send_bill: Annotated[Optional[bool], Field(None, alias='SendBill')]

        @field_validator('offer_url')
        @classmethod
        def validate_offer_url(cls, value: str, values) -> Optional[str]:
            if value is not None and not values.data.get(
                'preview_form',
                False,
            ):
                raise ValueError('You must specify PreviewForm = True.')
            return value

    class PaymentRequest(PaymentRequestBase):
        class ExtraData(ExtraDataBase):
            dynamic_amount: Annotated[
                Optional[bool],
                Field(None, alias='DynamicAmount'),
            ]

        extra_data: Annotated[
            Optional[ExtraData],
            Field(None, alias='ExtraData'),
        ]

    metadata: Annotated[Optional[MetaData], Field(None, alias='MetaData')]
    payment_request: Annotated[PaymentRequest, Field(alias='PaymentRequest')]


class PaylinkVoid(RequestIdSchema):
    id: Annotated[str, Field(alias='Id')]
