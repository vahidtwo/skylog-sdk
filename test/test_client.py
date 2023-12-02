from dataclasses import dataclass
from unittest import TestCase, mock

from skylog.client import AlertingSkyLogClient
from skylog.integration import AlertingProvider


@dataclass
class MockClientSettings:
    PROXY_USERNAME: str = ""
    PROXY_PASSWORD: str = ""
    PROXY_IP: str = ""
    PROXY_PORT: str = ""
    SKY_LOG_ALERTING_TELEGRAM_ALERT_NAME: str = ""
    SKY_LOG_ALERTING_PHONE_CALL_ALERT_NAME: str = ""
    SKY_LOG_ALERTING_SMS_ALERT_NAME: str = ""
    SKY_LOG_BASE_URL: str = ""
    SKY_LOG_ALERTING_TOKEN: str = ""


skylog_response = {
    "duplicate_instance": {
        "status": True,
        "message": "Already Active",
    },
    "success": {
        "status": True,
        "message": "Activated",
    },
    "stop_success": {
        "status": True,
        "message": "Stopped",
    },
    "notify_success": {
        "status": True,
        "message": "Done",
    },
}


class ClientTestCase(TestCase):
    def setUp(self):
        super().setUp()
        mock_retry = mock.patch("skylog.client.AlertingSkyLogClient.retry")
        self.mock_retry = mock_retry.start()
        self.provider = AlertingProvider(telegram="telegram", phone_call="phone_call", sms="sms")
        self.client = AlertingSkyLogClient(default_provider=self.provider.telegram, settings=MockClientSettings)  # noQa

    def tearDown(self):
        self.mock_retry.stop()

    def test_client_fire_issue(self):
        self.mock_retry.return_value.json.return_value = skylog_response["success"]
        self.mock_retry.return_value.status_code = 200
        status = self.client.fire_alert(description="test", instance_name="test_instance")
        self.assertTrue(status)

    def test_client_stop_issue(self):
        self.mock_retry.return_value.json.return_value = skylog_response["stop_success"]
        self.mock_retry.return_value.status_code = 200
        status = self.client.stop_alert(description="test", instance_name="test_instance")
        self.assertTrue(status)

    def test_client_notify_issue(self):
        self.mock_retry.return_value.json.return_value = skylog_response["notify_success"]
        self.mock_retry.return_value.status_code = 200
        status = self.client.notify(description="test", instance_name="test_instance")
        self.assertTrue(status)

    def test_notify_on_duplicate(self):
        self.mock_retry.return_value.json.return_value = skylog_response["duplicate_instance"]
        self.mock_retry.return_value.status_code = 200
        with mock.patch.object(self.client, "notify") as notify_mock:
            status = self.client.fire_alert(description="test", instance_name="test_instance", notify_on_duplicate=True)
            self.assertTrue(status)
        notify_mock.assert_called_once_with(
            description="test", instance_name="test_instance", summery=None, provider=None
        )
