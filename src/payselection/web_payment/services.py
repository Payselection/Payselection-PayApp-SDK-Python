from typing import Any
from typing import Dict

from requests import Response

from payselection.core.service import BaseService
from payselection.core.urls import WebUrlsBuilder
from payselection.web_payment.schema import CreatePaymentSchema
from payselection.web_payment.schema import PaylinkSchema
from payselection.web_payment.schema import PaylinkVoid


class WebPayment(BaseService):
    def __init__(self):
        super().__init__(WebUrlsBuilder())


class PayWidget(WebPayment):
    @classmethod
    def create(cls, params: Dict[str, Any]) -> Response:
        """
        A payment creation method that allows payment to be made
        """
        return cls().call_api(CreatePaymentSchema(**params))


class PayLink(WebPayment):
    @classmethod
    def create(cls, params: Dict[str, Any]) -> Response:
        """
        Allows to create a link to go to the payment widget
        """
        return cls().call_api(PaylinkSchema(**params))

    @classmethod
    def void(cls, params: Dict[str, Any]) -> Response:
        """
        Allows to cancel the link to the payment widget
        """
        return cls().call_api(PaylinkVoid(**params))
