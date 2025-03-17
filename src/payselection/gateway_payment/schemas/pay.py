from ipaddress import ip_address
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from langcodes import Language
from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from typing_extensions import Annotated

from payselection.core.enums import PaymentType
from payselection.core.schemas.receipt.receipt_data import ReceiptData
from payselection.core.schemas.schema import BaseSchema
from payselection.core.schemas.schema import CustomerInfo as CustomerInfoBase
from payselection.core.schemas.schema import OrderIdSchema
from payselection.core.schemas.schema import PayBase
from payselection.core.schemas.schema import PaymentRequestBase
from payselection.core.schemas.schema import RequestIdSchema
from payselection.core.schemas.schema import SplitData
from payselection.core.schemas.schema import TransactionIdSchema
from payselection.gateway_payment.enums import PaymentMethod
from payselection.gateway_payment.enums import TokenType
from payselection.recurring.schema import RebillIdSchema


class CryptogramValueSchema(BaseSchema):
    value: Annotated[str, Field(alias='Value')]


class TokenValueSchema(BaseSchema):
    type: Annotated[TokenType, Field(alias='Type')]
    pay_token: Annotated[str, Field(alias='PayToken')]


class PaySchema(PaymentRequestBase, RequestIdSchema):
    class CustomerInfo(CustomerInfoBase):
        is_send_receipt: Annotated[
            Optional[bool],
            Field(None, alias='IsSendReceipt'),
        ]
        ip: Annotated[str, Field(alias='IP')]

        @field_validator('ip')
        @classmethod
        def validate_ip(cls, value: str) -> str:
            ip_address(value)
            return value

    class ExtraData(BaseSchema):
        return_url: Annotated[
            Optional[HttpUrl],
            Field(None, alias='ReturnUrl'),
        ]
        webhook_url: Annotated[
            Optional[HttpUrl],
            Field(None, alias='WebhookUrl'),
        ]
        screen_height: Annotated[
            Optional[str],
            Field(
                None,
                pattern=r'^\d+$',
                alias='ScreenHeight',
            ),
        ]
        screen_width: Annotated[
            Optional[str],
            Field(
                None,
                pattern=r'^\d+$',
                alias='ScreenWidth',
            ),
        ]
        challenge_window_size: Annotated[
            Optional[Union[int, str]],
            Field(
                None,
                alias='ChallengeWindowSize',
            ),
        ]
        time_zone_offset: Annotated[
            Optional[Union[int, str]],
            Field(
                None,
                alias='TimeZoneOffset',
            ),
        ]
        color_depth: Annotated[
            Optional[Union[int, str]],
            Field(
                None,
                alias='ColorDepth',
            ),
        ]
        region: Annotated[Optional[str], Field(None, alias='Region')]
        user_agent: Annotated[Optional[str], Field(None, alias='UserAgent')]
        accept_header: Annotated[
            Optional[str],
            Field(None, alias='acceptHeader'),
        ]
        java_enabled: Annotated[bool, Field(False, alias='JavaEnabled')]
        java_script_enabled: Annotated[
            bool,
            Field(False, alias='javaScriptEnabled'),
        ]

        @field_validator('region')
        @classmethod
        def validate_region(cls, value: Optional[str]) -> Optional[str]:
            if value is None:
                return None
            if not Language.get(value).is_valid():
                raise ValueError('The field is invalid')
            return value

        @field_validator('time_zone_offset')
        @classmethod
        def validate_time_zone_offset(
            cls,
            value: Optional[int],
        ) -> Optional[str]:
            if value is None:
                return None

            if not (-840 <= value <= 840):
                raise ValueError(
                    f'Invalid time zone offset value: {value}.'
                    f' Values from -840 to 840 minutes are allowed.',
                )
            return str(value)

        @field_validator('color_depth')
        @classmethod
        def validate_color_depth(cls, value: Optional[int]) -> Optional[str]:
            if value is None:
                return None
            allowed_values = [1, 4, 8, 15, 16, 24, 32, 48]
            if value not in allowed_values:
                raise ValueError(
                    f'Invalid color depth value: {value}. '
                    f'Only {allowed_values} are allowed',
                )
            return str(value)

        @field_validator('challenge_window_size')
        @classmethod
        def validate_challenge_window_size(
            cls,
            value: Optional[int],
        ) -> Optional[str]:
            if value is None:
                return None
            allowed_values = [1, 2, 3, 4, 5]
            if value not in allowed_values:
                raise ValueError(
                    f'Invalid challenge window size value: {value}. '
                    f'Only {allowed_values} are allowed',
                )
            return str(value)

    rebill_flag: Annotated[Optional[bool], Field(None, alias='RebillFlag')]
    customer_info: Annotated[CustomerInfo, Field(alias='CustomerInfo')]
    extra_data: Annotated[Optional[ExtraData], Field(None, alias='ExtraData')]
    payment_method: Annotated[PaymentMethod, Field(alias='PaymentMethod')]
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]
    payment_details: Annotated[
        Optional[Union[CryptogramValueSchema, TokenValueSchema]],
        Field(
            default=None,
            alias='PaymentDetails',
        ),
    ]

    @field_validator('payment_details')
    @classmethod
    def validate_payment_details(cls, value, values):
        method = values.data['payment_method']
        method_to_details = {
            PaymentMethod.CRYPTOGRAM: CryptogramValueSchema,
            PaymentMethod.CRYPTOGRAM_RSA: CryptogramValueSchema,
            PaymentMethod.TOKEN: TokenValueSchema,
        }
        if method not in method_to_details:
            return None
        expected_model = method_to_details[method]
        if not isinstance(value, expected_model):
            raise ValueError('Payment does not match the expected model')
        return value


class RebillSchema(PaymentRequestBase, RequestIdSchema):
    rebill_flag: Annotated[Optional[bool], Field(None, exclude=True)]
    rebill_id: Annotated[str, Field(alias='RebillId')]
    payment_type: Annotated[
        Optional[PaymentType],
        Field(None, alias='PaymentType'),
    ]
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    webhook_url: Annotated[Optional[HttpUrl], Field(None, alias='WebhookUrl')]
    extra_data: Annotated[
        Optional[Dict[str, Any]],
        Field(None, alias='ExtraData'),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]


class ConfirmSchema(OrderIdSchema, TransactionIdSchema, RequestIdSchema):
    payment_response: Annotated[str, Field(alias='PaRes')]
    md: Annotated[str, Field(alias='MD')]


class RefundSchema(PayBase, RequestIdSchema):
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    webhook_url: Annotated[Optional[HttpUrl], Field(None, alias='WebhookUrl')]


class CancelSchema(PayBase, RequestIdSchema):
    webhook_url: Annotated[Optional[HttpUrl], Field(None, alias='WebhookUrl')]


class ChargeSchema(PayBase, RequestIdSchema):
    webhook_url: Annotated[Optional[HttpUrl], Field(None, alias='WebhookUrl')]
    receipt_data: Annotated[
        Optional[ReceiptData],
        Field(None, alias='ReceiptData'),
    ]
    split_data: Annotated[
        Optional[List[SplitData]],
        Field(None, alias='SplitData'),
    ]


class Unsubscribe(RebillIdSchema, RequestIdSchema):
    pass
