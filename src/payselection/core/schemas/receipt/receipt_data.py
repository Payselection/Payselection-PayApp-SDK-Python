from datetime import datetime
from decimal import Decimal
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl
from pydantic import UrlConstraints
from typing_extensions import Annotated

from payselection.core.enums import AgentType
from payselection.core.enums import PaymentObject
from payselection.core.enums import SNO
from payselection.core.schemas.receipt.item import ItemBase
from payselection.core.schemas.schema import PhonesSchema


class AgentInfo(BaseModel):
    class PayingAgent(PhonesSchema):
        operation: Annotated[Optional[str], Field(None, max_length=24)]

    class ReceivePaymentsOperator(PhonesSchema):
        pass

    class MoneyTransferOperator(PhonesSchema):
        name: Annotated[Optional[str], Field(None, max_length=64)]
        address: Annotated[Optional[str], Field(None, max_length=256)]
        inn: Annotated[
            Optional[str],
            Field(
                None,
                pattern=r'(^[0-9]{10}$)|(^[0-9]{12}$)',
            ),
        ]

    type: Annotated[Optional[AgentType], Field(default=None)]
    paying_agent: Annotated[Optional[PayingAgent], Field(default=None)]
    receive_payments_operator: Annotated[
        Optional[ReceivePaymentsOperator],
        Field(default=None),
    ]
    money_transfer_operator: Annotated[
        Optional[MoneyTransferOperator],
        Field(default=None),
    ]


class BaseCompany(BaseModel):
    email: Annotated[Optional[EmailStr], Field(default=None, max_length=64)]
    sno: Annotated[Optional[SNO], Field(default=None)]
    inn: Annotated[str, Field(pattern=r'(^[0-9]{10}$)|(^[0-9]{12}$)')]
    payment_address: Annotated[
        HttpUrl,
        UrlConstraints(max_length=256),
    ]


class BaseFFD(BaseModel):
    class Client(BaseModel):
        name: Annotated[Optional[str], Field(None, max_length=256)]
        inn: Annotated[
            Optional[str],
            Field(
                default=None,
                pattern=r'(^[0-9]{10}$)|(^[0-9]{12}$)',
            ),
        ]
        email: Annotated[
            Optional[EmailStr],
            Field(default=None, max_length=64),
        ]
        phone: Annotated[
            Optional[str],
            Field(
                None,
                max_length=64,
                pattern=r'^\+?\d*$',
            ),
        ]

        @field_validator('phone')
        @classmethod
        def validate_phone(cls, value: Optional[str], values) -> Optional[str]:
            if value is None and values.data.get('email') is None:
                raise ValueError(
                    'At least one of the fields must be'
                    ' filled in: email or phone.',
                )
            return value

    class Item(ItemBase):
        payment_object: PaymentObject
        nomenclature_code: Annotated[
            Optional[str],
            Field(None, max_length=150),
        ]

    class Payment(BaseModel):
        type: Annotated[int, Field(ge=0, le=4)]
        sum: Annotated[Decimal, Field(ge=0, lt=99999999.99, decimal_places=2)]

    class AdditionalUserProps(BaseModel):
        name: Annotated[str, Field(max_length=64)]
        value: Annotated[str, Field(max_length=256)]

    client: Client
    company: BaseCompany
    items: Annotated[List[Item], Field(min_length=1, max_length=100)]
    payments: Annotated[
        List[Payment],
        Field(
            min_length=1,
            max_length=10,
        ),
    ]
    total: Annotated[Decimal, Field(ge=0, lt=99999999.99, decimal_places=2)]
    additional_check_props: Annotated[
        Optional[str],
        Field(None, max_length=16),
    ]
    cashier: Annotated[Optional[str], Field(None, max_length=64)]
    additional_user_props: Annotated[
        Optional[AdditionalUserProps],
        Field(default=None),
    ]


class ReceiptData(BaseModel):
    timestamp: str
    external_id: Annotated[Optional[str], Field(None, max_length=128)]
    receipt: BaseFFD

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
            return value
        except ValueError:
            raise ValueError('The data must be in format: dd.mm.yyyy HH:MM:SS')
