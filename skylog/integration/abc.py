from abc import ABC, abstractmethod
from typing import Optional

from skylog.integration import AlertingProvider
from skylog.integration.utils import BaseClient, RetryMixin


class BaseAlertingSkyLogClient(RetryMixin, BaseClient, ABC):
    """
    client to send alert to skylog
    """

    @abstractmethod
    def fire_alert(
        self,
        description: str,
        *,
        instance_name: str = None,
        summery=None,
        provider: Optional[AlertingProvider] = None,
        notify_on_duplicate: bool = False,
    ) -> bool:
        """
        firing an alert cause to add a record in triggered list in the panel and Immediately notice messages are sent
         to related endpoints.
        """

    @abstractmethod
    def stop_alert(
        self,
        description: str,
        *,
        instance_name: str = None,
        summery: str = None,
        provider: Optional[AlertingProvider] = None,
        notify_on_duplicate: bool = False,
    ) -> bool:
        """
        Stopping a fired alert cause remove its record in triggered list furthermore
        it's solving message are sent to endpoints.
        This procedure can be done manually in the panel or automatically by api call.
        """

    @abstractmethod
    def notify(
        self,
        description: str,
        instance_name: str = None,
        summery: str = None,
        *,
        provider: Optional[AlertingProvider] = None,
    ) -> bool:
        """
        Stopping a fired alert cause remove its record in triggered list furthermore
        it's solving issue that sent to endpoints.
        This procedure can be done manually in the panel or automatically by api call.
        """

    @abstractmethod
    def _request(
        self,
        description: str,
        instance_name: str,
        summery: str,
        path: str,
        *,
        provider: Optional[AlertingProvider] = None,
        notify_on_duplicate: bool = False,
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
