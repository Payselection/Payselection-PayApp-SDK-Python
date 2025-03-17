import inspect
import urllib.parse
from typing import Tuple

import requests
from pydantic import BaseModel
from requests import Response

from payselection.core.configuration import Configuration
from payselection.core.exceptions.api_error import APIError
from payselection.core.exceptions.api_error import InvalidCallerAPI
from payselection.core.urls import UrlsBuilder
from payselection.core.urls import WebUrlsBuilder
from payselection.core.utils.signature_formation import get_signature


class ApiClient:
    def __init__(
        self,
        config: Configuration,
        urls_builder: UrlsBuilder,
    ):
        self.site_id = config.site_id
        self.secret_key = config.secret_key
        self.public_key = config.public_key
        self.merchant_url_address = str(config.merchant_url_address)
        self._urls_builder = urls_builder
        self.timeout = config.timeout

    def _call(self, params: BaseModel, *args, **kwargs) -> Response:
        method, endpoint, api_chapter = self._caller()
        signature_key = (
            self.public_key
            if isinstance(self._urls_builder, WebUrlsBuilder)
            else self.secret_key
        )
        raw_body = params.model_dump_json(by_alias=True, exclude_none=True)

        path_param = kwargs.get('path_param')
        if path_param is not None:
            endpoint = endpoint.format(**path_param)
        url_for_signature = endpoint
        if api_chapter == 'PayLink':
            url_for_signature = self.merchant_url_address

        headers = self._build_headers(
            method,
            url_for_signature,
            raw_body,
            signature_key,
            params.request_id,
        )

        url = urllib.parse.urljoin(
            self._urls_builder.BASE_URL.rstrip('/') + '/',
            endpoint.lstrip('/'),
        )
        response = requests.request(
            method.lower(),
            url,
            data=raw_body,
            timeout=self.timeout,
            headers=headers,
        )
        return self._handle_response(response)

    def _handle_response(self, response: Response) -> Response:
        if response.ok:
            return response

        try:
            result = response.json()
            error_code = result.get('Code')
            description = result.get('Description')
            if error_code is None:
                error_code = 'Bad Request'
                description = result.get('message')
            exception_class = type(error_code, (APIError,), {})
            raise exception_class(
                response.status_code,
                error_code,
                description,
                result.get('AddDetails'),
            )

        except ValueError:
            raise APIError(
                response.status_code,
                'UnknownError',
                'Invalid response format',
                {},
            )

    def _build_headers(
        self,
        method: str,
        endpoint: str,
        raw_body: str,
        signature_key: str,
        request_id: str,
    ) -> dict:
        headers = {
            'X-SITE-ID': str(self.site_id),
            'X-REQUEST-ID': request_id,
            'X-REQUEST-SIGNATURE': get_signature(
                method,
                endpoint,
                self.site_id,
                raw_body,
                signature_key,
                request_id=request_id,
            ),
        }

        return headers

    def _caller(self) -> Tuple[str, str, str]:
        frame = inspect.stack()[3]
        api_chapter = frame.frame.f_locals['cls'].__name__
        api_method = frame.function
        if api_chapter == 'Pay' and api_method == 'get_public_key':
            api_chapter = frame.frame.f_locals['cls'].mro()[1].__name__
        try:
            caller_method, caller_endpoint = self._urls_builder.ENDPOINTS[
                api_chapter
            ][api_method]
        except Exception:
            raise InvalidCallerAPI('Check stack of call')

        return caller_method, caller_endpoint, api_chapter
