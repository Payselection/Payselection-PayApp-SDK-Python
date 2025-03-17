from typing import Any
from typing import Dict
from typing import Optional
from uuid import uuid4

from requests import Response

from payselection.core.configuration import Configuration
from payselection.core.schemas.schema import RequestIdSchema
from payselection.core.service import BaseService
from payselection.core.urls import GatewayUrlsBuilder
from payselection.core.utils.cryptogram_formation import (
    encrypt_data_for_cryptogram,
)
from payselection.core.utils.cryptogram_formation import (
    encrypt_data_for_cryptogram_rsa,
)
from payselection.gateway_payment.enums import PaymentMethod
from payselection.gateway_payment.schemas.card_data import CardDataSchema
from payselection.gateway_payment.schemas.pay import CancelSchema
from payselection.gateway_payment.schemas.pay import ChargeSchema
from payselection.gateway_payment.schemas.pay import ConfirmSchema
from payselection.gateway_payment.schemas.pay import PaySchema
from payselection.gateway_payment.schemas.pay import RebillSchema
from payselection.gateway_payment.schemas.pay import RefundSchema
from payselection.gateway_payment.schemas.pay import Unsubscribe
from payselection.gateway_payment.schemas.payout import PayoutSchema
from payselection.gateway_payment.schemas.schema import OrderIdRequestSchema
from payselection.gateway_payment.schemas.schema import (
    TransactionRequestIdSchema,
)
from payselection.gateway_payment.schemas.schema import (
    TransactionsByDatesSchema,
)


class GatewayPayment(BaseService):
    PUBLIC_KEY: str = 'public_key'

    def __init__(self):
        super().__init__(GatewayUrlsBuilder())

    @classmethod
    def get_public_key(cls, params: Dict[str, Any]) -> Response:
        """Obtains a public key for generating
        a cryptogram using the CardRSAToken library"""
        return cls().call_api(RequestIdSchema(**params))

    @classmethod
    def get_sbp_members(cls, params: Dict[str, Any]) -> Response:
        """Receives deeplink (fast payments system, ru: СБП)."""
        return cls().call_api(
            RequestIdSchema(**{'request_id': params.pop('request_id')}),
            path_param=TransactionRequestIdSchema(**params).model_dump(),
        )

    @classmethod
    def get_cryptogram(
        cls,
        params: Dict[str, Any],
    ) -> str:
        """Gets Public Key for Cryptogram"""
        card_data = CardDataSchema(**params)
        raw_data = card_data.model_dump_json(by_alias=True, exclude_none=True)
        return encrypt_data_for_cryptogram(
            raw_data.encode(),
            Configuration.public_key,
        )

    @classmethod
    def get_cryptogram_rsa(
        cls,
        request_id: Dict[str, str],
        params: Dict[str, Any],
    ) -> str:
        """Gets RSA Public Key"""
        public_key = cls().get_public_key(request_id).json()[cls.PUBLIC_KEY]
        raw_data = CardDataSchema(**params).model_dump_json(
            by_alias=True,
            exclude_none=True,
        )
        return encrypt_data_for_cryptogram_rsa(
            raw_data.encode(),
            public_key,
        )


class CheckTransactionStatus(GatewayPayment):
    @classmethod
    def check_by_order_id(cls, params: Dict[str, Any]) -> Response:
        """
        Obtains information about
        the current status of the OrderId order identifier
        """
        return cls().call_api(
            RequestIdSchema(**{'request_id': params.pop('request_id')}),
            path_param=OrderIdRequestSchema(**params).model_dump(),
        )

    @classmethod
    def check_by_transaction_id(cls, params: Dict[str, Any]) -> Response:
        """
        Obtains information about
        the current status of the transaction ID TransactionId
        """
        return cls().call_api(
            RequestIdSchema(**{'request_id': params.pop('request_id')}),
            path_param=TransactionRequestIdSchema(**params).model_dump(),
        )

    @classmethod
    def check_by_order_id_extended(cls, params: Dict[str, Any]) -> Response:
        """
        An advanced query is used to obtain information
        about the current status by orderId
        """
        return cls().call_api(
            RequestIdSchema(**{'request_id': params.pop('request_id')}),
            path_param=OrderIdRequestSchema(**params).model_dump(),
        )

    @classmethod
    def check_by_transaction_id_extended(
        cls,
        params: Dict[str, Any],
    ) -> Response:
        """
        An advanced query is used to obtain information about
         the current status of the transaction ID TransactionId
        """
        return cls().call_api(
            RequestIdSchema(**{'request_id': params.pop('request_id')}),
            path_param=TransactionRequestIdSchema(**params).model_dump(),
        )

    @classmethod
    def check_by_dates(cls, params: Dict[str, Any]) -> Response:
        """An advanced query is used to obtain
        the status of transactions for a selected date range"""
        return cls().call_api(TransactionsByDatesSchema(**params))


class Pay(GatewayPayment):
    @classmethod
    def add_cryptogram(
        cls,
        params: Dict[str, Any],
        card_data: Dict[str, Any],
    ) -> None:
        payment_method = params['payment_method']
        cryptogram = {'value': None}
        if payment_method == PaymentMethod.CRYPTOGRAM:
            cryptogram['value'] = cls.get_cryptogram(card_data)

        if payment_method == PaymentMethod.CRYPTOGRAM_RSA:
            cryptogram['value'] = cls.get_cryptogram_rsa(
                {'request_id': uuid4().hex},
                card_data,
            )

        params['payment_details'] = cryptogram

    @classmethod
    def pay(
        cls,
        params: Dict[str, Any],
        card_data: Optional[Dict[str, Any]],
    ) -> Response:
        """
        Direct writing off from the client's card
        """
        if card_data is not None:
            cls.add_cryptogram(params, card_data)
        return cls().call_api(PaySchema(**params))

    @classmethod
    def block(
        cls,
        params: Dict[str, Any],
        card_data: Optional[Dict[str, Any]],
    ) -> Response:
        """Two-step payment is a payment consisting of two operations:
        holding funds on the card and completing authorization (debiting)."""
        if card_data is not None:
            cls.add_cryptogram(params, card_data)
        return cls().call_api(PaySchema(**params))

    @classmethod
    def rebill(cls, params: Dict[str, Any]) -> Response:
        """Records funds on a card that was previously saved via RebillId."""
        return cls().call_api(RebillSchema(**params))

    @classmethod
    def confirm(cls, params: Dict[str, Any]) -> Response:
        """Completes the withdrawal of funds from the card by single-stage
        (Pay) and two-stage (Block) payment operations after receiving
        the 3D-Secure authentication result from the Bank"""
        return cls().call_api(ConfirmSchema(**params))

    @classmethod
    def refund(cls, params: Dict[str, Any]) -> Response:
        """Returns funds that were debited using
        a one-step Pay or two-step Block payment operation"""
        return cls().call_api(RefundSchema(**params))

    @classmethod
    def cancel(cls, params: Dict[str, Any]) -> Response:
        """Full cancels the blocking of funds
        during a two-step payment Block"""
        return cls().call_api(CancelSchema(**params))

    @classmethod
    def charge(cls, params: Dict[str, Any]) -> Response:
        """Writes off funds from a card as part of a previously held holding"""
        return cls().call_api(ChargeSchema(**params))

    @classmethod
    def unsubscribe(cls, params: Dict[str, Any]) -> Response:
        """Deactivates a unique RebillId (token)."""
        return cls().call_api(Unsubscribe(**params))


class Payout(GatewayPayment):
    @classmethod
    def payout(cls, params: Dict[str, Any]) -> Response:
        """Original credit transaction (OCT) is a type of transaction
        in which funds are transferred to bank cards for individuals"""
        return cls().call_api(PayoutSchema(**params))

    @classmethod
    def balance(cls, params: Dict[str, Any]) -> Response:
        """Checks available balance for Payout."""
        return cls().call_api(RequestIdSchema(**params))
