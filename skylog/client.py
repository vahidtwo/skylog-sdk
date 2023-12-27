import logging
from typing import Optional

from requests import Response

from .exception import RetryException
from .integration.abc import BaseAlertingSkyLogClient
from .integration.config import LazySettings
from .integration.utils import BaseClient, RetryMixin

logger = logging.getLogger(__name__)


class AlertingSkyLogClient(BaseAlertingSkyLogClient, RetryMixin, BaseClient):
    """
    client to send alert to skylog


    usage:
        >>> client = AlertingSkyLogClient(instance_name='shaparak-ftp', default_provider=AlertingProvider.telegram)
        >>> client.fire_alert(description="test")
    you can determine provider to send data to that alert with a specific endpoint
    at this time this there are 2 kinds of allert, Telegram, Phone call, SMS,
    you can use any of them for sending allert, you can set it in class instance constractor,
     method call parameter
    the priority of set alert name : first check method provider parameter, if it is not set check class variable
    """

    duplicate_request_message = "Already Active"
    alert_instance_not_exists = "Alert Instance Doesn't Exists"

    base_url = ...

    def __init__(
        self,
        instance_name: str = "default",
        *,
        default_provider: str,
        use_proxy: bool = False,
        settings: Optional[LazySettings] = None,
        enable: bool = True,
        **kwargs,
    ):
        if settings is None:
            try:
                from django.conf import settings
            except ImportError:
                from skylog.integration.config import settings
        self.base_url = settings.SKY_LOG_ALERTING_BASE_URL
        self.token = settings.SKY_LOG_ALERTING_TOKEN
        self.token_type = "Bearer"
        self._instance_name = instance_name
        self.provider = default_provider
        self.use_proxy = use_proxy
        self.settings = settings
        self.enable = enable
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__(settings=settings)

    def fire_alert(
        self,
        description: str,
        *,
        instance_name: str = None,
        summery=None,
        provider: Optional[str] = None,
        notify_on_duplicate: bool = False,
        _notify_instance_name: Optional[str] = None,
    ) -> bool:
        """
        firing an alert cause to add a record in triggered list in the panel and Immediately notice messages are sent
         to related endpoints.
        """
        return self._request(
            description=description,
            instance_name=instance_name,
            summery=summery,
            path="fire-alert",
            provider=provider,
            notify_on_duplicate=notify_on_duplicate,
            _notify_instance_name=_notify_instance_name,
        )

    def stop_alert(
        self,
        description: str,
        *,
        instance_name: str = None,
        summery: str = None,
        provider: Optional[str] = None,
        notify_on_duplicate: bool = False,
    ) -> bool:
        """
        Stopping a fired alert cause remove its record in triggered list furthermore
        it's solving message are sent to endpoints.
        This procedure can be done manually in the panel or automatically by api call.
        """
        return self._request(
            description=description,
            instance_name=instance_name,
            summery=summery,
            path="stop-alert",
            provider=provider,
            notify_on_duplicate=notify_on_duplicate,
        )

    def notify(
        self,
        description: str,
        instance_name: str = None,
        summery: str = None,
        *,
        provider: Optional[str] = None,
    ) -> bool:
        """
        Stopping a fired alert cause remove its record in triggered list furthermore
        it's solving issue that sent to endpoints.
        This procedure can be done manually in the panel or automatically by api call.
        """
        return self._request(
            description=description,
            instance_name=instance_name,
            summery=summery,
            path="notification-alert",
            provider=provider,
            notify_on_duplicate=False,
        )

    def _request(
        self,
        description: str,
        instance_name: str,
        summery: str,
        path: str,
        *,
        provider: Optional[str] = None,
        notify_on_duplicate: bool = False,
        _notify_instance_name: Optional[str] = None,
    ) -> bool:
        """
        Parameter:
            alert_name: (required) the alert_name of created alert_rule.
            Instance: (required) instance of a group alert.
                In detail instance use to determine a specific part of a universal alert.
                For example, in "Database Down" alert rule instance can be "DB_Slave1" or for "low SMS credit"
                instance can be "Mobtakeran"
            description: all description need to explain the situation more.
            summery: summery to explain the situation more.

        """

        headers = {"Authorization": f"{self.token_type} {self.token}"}
        data = {
            "alertname": provider or self.provider,
            "instance": instance_name or self._instance_name,
            "description": description,
            "summery": summery,
        }
        if not self.enable:
            logger.warning(f"Alerting {instance_name}. {description}")
            return True

        def __request():
            return self.request(headers=headers, json=data, path=path)

        try:
            response: Response = self.retry(__request)
        except RetryException as e:
            logger.error(
                "retry send alerting skylog exception",
                extra={
                    "alert_name": provider,
                    "instance": instance_name,
                    "description": description,
                    "exception": str(e),
                },
                stack_info=True,
            )
            return False
        if response.status_code != 200:
            return False
        data = response.json()
        if notify_on_duplicate and data.get("message") == self.duplicate_request_message:
            description = self.get_notify_on_duplicated_message(description)
            return self.notify(
                description=description,
                instance_name=_notify_instance_name or instance_name,
                summery=summery,
                provider=provider,
            )
        if data["status"] is False and data.get("message") != self.alert_instance_not_exists:
            logger.error(
                "failed to send alerting skylog",
                extra={
                    "skylog_message": data.get("message"),
                    "alert_name": provider,
                    "instance": instance_name,
                    "description": description,
                },
            )
            return False
        return True

    @staticmethod
    def get_notify_on_duplicated_message(description: str, extra_info: Optional[str] = None) -> str:
        return f"{description} \n {extra_info}" if extra_info is not None else description
