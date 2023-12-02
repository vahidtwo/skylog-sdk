from typing import Callable, Any, Type

from requests import Session, Request

from skylog.exception import RetryException
from skylog.integration.config import LazySettings


class RetryMixin:
    """
    A class to implement the retrying process with the simple for loop.
    """

    @staticmethod
    def retry(block: Callable, count: int = 3, **kwargs) -> Any:
        """
        Raises:
            - RetryException
        """
        last_exception = None
        for _ in range(count):
            try:
                return block(**kwargs)
            except Exception as e:
                last_exception = e
        raise RetryException(count=count) from last_exception


class BaseClient:
    base_url = ""
    use_proxy = True
    verify_ssl = True
    requests_timeout = 30

    def __init__(self, settings: Type[LazySettings]):
        self.proxy_username = self.clean_string(settings.PROXY_USERNAME)
        self.proxy_password = self.clean_string(settings.PROXY_PASSWORD)
        self.proxy_ip = self.clean_string(settings.PROXY_IP)
        self.proxy_port = self.clean_string(settings.PROXY_PORT)
        self.session = self.create_session()

    @staticmethod
    def clean_string(string):
        return string.strip(" \n")

    def create_session(self):
        session = Session()
        session.verify = self.verify_ssl
        if self.use_proxy:
            session.proxies = self.create_proxy()
        return session

    def create_proxy(self):
        url = "http://{username}:{password}@{ip}:{port}".format(
            username=self.proxy_username,
            password=self.proxy_password,
            ip=self.proxy_ip,
            port=self.proxy_port,
        )
        return {"http": url, "https": url, "ftp": url}

    def request(
        self,
        url=None,
        path="",
        method="post",
        params=None,
        data=None,
        headers=None,
        proxy=None,
        auth=None,
        json=None,
    ):
        url = url or f"{self.base_url}{path}"
        self.session.proxies = proxy or self.session.proxies
        req = Request(method, url, params=params, data=data, auth=auth, json=json, headers=headers)
        prepared = req.prepare()
        return self.session.send(prepared, timeout=self.requests_timeout)
