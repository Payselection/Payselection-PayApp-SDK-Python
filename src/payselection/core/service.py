from pydantic import BaseModel
from requests import Response

from payselection.core.client import ApiClient
from payselection.core.configuration import Configuration
from payselection.core.urls import UrlsBuilder


class BaseService:
    def __init__(self, urls_builder: UrlsBuilder):
        config: Configuration = Configuration()
        self.client = ApiClient(config, urls_builder=urls_builder)

    def call_api(self, params: BaseModel, *args, **kwargs) -> Response:
        return self.client._call(params, *args, **kwargs)
