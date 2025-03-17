from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from typing_extensions import Annotated

from payselection.core.enums import AgentType
from payselection.core.enums import PaymentMethod
from payselection.core.enums import VatType
from payselection.core.schemas.schema import PhonesSchema


class VatBase(BaseModel):
    sum: Annotated[Decimal, Field(None, ge=0, lt=100000000, decimal_places=2)]


class VatRequiredType(VatBase):
    type: VatType


class VatAllRequired(VatRequiredType):
    sum: Annotated[Decimal, Field(ge=0, lt=100000000, decimal_places=2)]


class ItemBase(BaseModel):
    class AgentInfo(BaseModel):
        class PayingAgent(PhonesSchema):
            operation: Annotated[Optional[str], Field(default=None)]

        class ReceivePaymentsOperator(PhonesSchema):
            pass

        class MoneyTransferOperator(PhonesSchema):
            name: Annotated[Optional[str], Field(None, max_length=64)]
            address: Annotated[Optional[str], Field(None, max_length=256)]
            inn: Annotated[
                Optional[str],
                Field(
                    default=None,
                    pattern=r'(^[0-9]{10}$)|(^[0-9]{12}$)',
                ),
            ]

        type: Annotated[Optional[AgentType], Field(default=None)]
        paying_agent: Annotated[Optional[PayingAgent], Field(default=None)]
        receive_payments_operator: Annotated[
            Optional[ReceivePaymentsOperator],
            Field(
                default=None,
            ),
        ]
        money_transfer_operator: Annotated[
            Optional[MoneyTransferOperator],
            Field(
                default=None,
            ),
        ]

    class SupplierInfo(PhonesSchema):
        pass

    name: Annotated[str, Field(max_length=128)]
    price: Annotated[Decimal, Field(ge=0, le=42949672.95, decimal_places=2)]
    quantity: Annotated[Decimal, Field(ge=0, lt=100000, decimal_places=3)]
    sum: Annotated[Decimal, Field(ge=0, le=42949672.95, decimal_places=3)]
    measurement_unit: Annotated[Optional[str], Field(None, max_length=16)]
    payment_method: PaymentMethod
    vat: VatRequiredType
    agent_info: Annotated[Optional[AgentInfo], Field(default=None)]
    supplier_info: Annotated[Optional[SupplierInfo], Field(default=None)]
    user_data: Annotated[Optional[str], Field(None, max_length=64)]
    excise: Annotated[
        Decimal,
        Field(
            None,
            ge=0,
            decimal_places=2,
            max_digits=10,
        ),
    ]
    country_code: Annotated[
        Optional[str],
        Field(
            None,
            min_length=1,
            max_length=3,
            pattern='^[0-9]*$',
        ),
    ]
    declaration_number: Annotated[
        Optional[str],
        Field(
            None,
            min_length=1,
            max_length=32,
        ),
    ]

    @field_validator('supplier_info')
    @classmethod
    def validate_supplier_info(cls, value, values):
        if values.data.get('agent_info') is not None and value is None:
            raise ValueError(
                "parameter 'supplier_info' is required, "
                "if 'agent_info' is specified",
            )
        return value
