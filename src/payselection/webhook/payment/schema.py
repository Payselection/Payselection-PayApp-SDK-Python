from datetime import datetime
from typing import List
from typing import Optional

from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from typing_extensions import Annotated

from payselection.core.schemas.schema import OrderIdSchema
from payselection.core.schemas.schema import PayBase
from payselection.core.schemas.schema import SplitData
from payselection.gateway_payment.schemas.payout import CARD_HOLDER_PATTERN
from payselection.webhook.payment.enum import Event
from payselection.webhook.payment.enum import PaymentMethod


class EventWebhookBase(PayBase, OrderIdSchema):
    event: Annotated[Event, Field(alias='Event')]
    datetime: Annotated[str, Field(alias='DateTime')]
    service_id: Annotated[
        str,
        Field(min_length=1, max_length=12, alias='Service_Id'),
    ]
    is_test: Annotated[int, Field(alias='IsTest')]
    gate: Annotated[Optional[str], Field(None, alias='Gate')]
    bank: Annotated[Optional[str], Field(None, alias='Bank')]
    country_code_alpha2: Annotated[
        Optional[str],
        Field(
            None,
            min_length=2,
            max_length=2,
            alias='Country_Code_Alpha2',
        ),
    ]
    brand: Annotated[Optional[str], Field(None, alias='Brand')]
    custom_fields: Annotated[
        Optional[str],
        Field(
            None,
            min_length=1,
            max_length=8096,
            alias='CustomFields',
        ),
    ]
    phone: Annotated[
        Optional[str],
        Field(
            None,
            min_length=8,
            max_length=20,
            alias='Phone',
        ),
    ]
    email: Annotated[Optional[EmailStr], Field(None, alias='Email')]
    description: Annotated[
        Optional[str],
        Field(
            None,
            min_length=1,
            max_length=250,
            alias='Description',
        ),
    ]
    subtype: Annotated[Optional[str], Field(None, alias='Subtype')]
    expiration_date: Annotated[
        Optional[str],
        Field(None, alias='ExpirationDate'),
    ]
    card_masked: Annotated[
        str,
        Field(min_length=12, max_length=19, alias='CardMasked'),
    ]
    card_holder: Annotated[
        Optional[str],
        Field(
            None,
            min_length=1,
            max_length=30,
            pattern=CARD_HOLDER_PATTERN,
            alias='CardHolder',
        ),
    ]
    rrn: Annotated[Optional[str], Field(None, alias='RRN')]

    @field_validator('datetime')
    @classmethod
    def validate_timestamp(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%d.%m.%Y %H.%M.%S')
            return value
        except ValueError:
            raise ValueError('The data must be in format: dd.mm.yyyy HH.MM.SS')


class PaymentEventWebhook(EventWebhookBase):
    payment_method: Annotated[
        PaymentMethod,
        Field(None, alias='PaymentMethod'),
    ]
    payout_token: Annotated[Optional[str], Field(None, alias='PayoutToken')]
    rebill_id: Annotated[Optional[str], Field(None, alias='RebillId')]
    recurring_id: Annotated[Optional[str], Field(None, alias='RecurringId')]
    qr_code_string: Annotated[Optional[str], Field(None, alias='QrCodeString')]
    sber_string: Annotated[Optional[str], Field(None, alias='SberString')]
    sber_deep_link: Annotated[Optional[str], Field(None, alias='SberDeepLink')]
    card_masked: Annotated[
        Optional[str],
        Field(
            None,
            min_length=12,
            max_length=19,
            alias='CardMasked',
        ),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]


class BlockEventWebhook(EventWebhookBase):
    payment_method: Annotated[
        Optional[PaymentMethod],
        Field(None, alias='PaymentMethod'),
    ]
    payout_token: Annotated[Optional[str], Field(None, alias='PayoutToken')]
    rebill_id: Annotated[
        Optional[str],
        Field(
            None,
            min_length=16,
            max_length=16,
            alias='RebillId',
        ),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]


class FailEventWebhook(EventWebhookBase):
    payment_method: Annotated[
        Optional[PaymentMethod],
        Field(None, alias='PaymentMethod'),
    ]
    error_message: Annotated[Optional[str], Field(None, alias='ErrorMessage')]
    error_code: Annotated[Optional[str], Field(None, alias='ErrorCode')]
    client_message: Annotated[
        Optional[str],
        Field(None, alias='ClientMessage'),
    ]
    qr_code_string: Annotated[Optional[str], Field(None, alias='QrCodeString')]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]


class RefundEventWebhook(EventWebhookBase):
    new_amount: Annotated[str, Field(alias='NewAmount')]


class CancelEventWebhook(EventWebhookBase):
    pass


class ThreeDSEventWebhook(EventWebhookBase):
    acs_url: Annotated[HttpUrl, Field(alias='AcsUrl')]
    pa_req: Annotated[str, Field(alias='PaReq')]
    md: Annotated[str, Field(alias='MD')]
    expiration_date: Annotated[str, Field(None, exclude=True)]
    card_masked: Annotated[str, Field(None, exclude=True)]
    card_holder: Annotated[str, Field(None, exclude=True)]
    rrn: Annotated[str, Field(None, exclude=True)]


class PayoutEventWebhook(EventWebhookBase):
    payout_token: Annotated[Optional[str], Field(None, alias='PayoutToken')]


class Redirect3DSEventWebhook(EventWebhookBase):
    redirect_method: Annotated[
        Optional[str],
        Field(None, alias='RedirectMethod'),
    ]
    redirect_url: Annotated[
        Optional[HttpUrl],
        Field(None, alias='RedirectUrl'),
    ]
    subtype: Annotated[None, Field(None, exclude=True)]
    expiration_date: Annotated[None, Field(None, exclude=True)]
    card_masked: Annotated[None, Field(None, exclude=True)]
    card_holder: Annotated[None, Field(None, exclude=True)]
    rrn: Annotated[None, Field(None, exclude=True)]


EVENT_SCHEMAS = {
    Event.PAYMENT: PaymentEventWebhook,
    Event.BLOCK: BlockEventWebhook,
    Event.FAIL: FailEventWebhook,
    Event.REFUND: RefundEventWebhook,
    Event.CANCEL: CancelEventWebhook,
    Event.THREEDS: ThreeDSEventWebhook,
    Event.PAYOUT: PaymentEventWebhook,
    Event.REDIRECT_3DS: Redirect3DSEventWebhook,
}
