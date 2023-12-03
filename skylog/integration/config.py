import dataclasses

from decouple import config


class ClientSettings:
    PROXY_USERNAME: str = None
    PROXY_PASSWORD: str = None
    PROXY_IP: str = None
    PROXY_PORT: str = None
    SKY_LOG_ALERTING_TELEGRAM_ALERT_NAME: str = None
    SKY_LOG_ALERTING_PHONE_CALL_ALERT_NAME: str = None
    SKY_LOG_ALERTING_SMS_ALERT_NAME: str = None
    SKY_LOG_ALERTING_BASE_URL: str = None
    SKY_LOG_ALERTING_TOKEN: str = None

    def _setup(self):
        self.PROXY_USERNAME = config("PROXY_USERNAME", "")
        self.PROXY_PASSWORD = config("PROXY_PASSWORD", "")
        self.PROXY_IP = config("PROXY_IP", "")
        self.PROXY_PORT = config("PROXY_PORT", "")
        self.DEFAULT_SKY_LOG_ALERTING_TELEGRAM_ALERT_NAME = config("DEFAULT_SKY_LOG_ALERTING_TELEGRAM_ALERT_NAME")
        self.DEFAULT_SKY_LOG_ALERTING_PHONE_CALL_ALERT_NAME = config("DEFAULT_SKY_LOG_ALERTING_PHONE_CALL_ALERT_NAME")
        self.DEFAULT_SKY_LOG_ALERTING_SMS_ALERT_NAME = config("DEFAULT_SKY_LOG_ALERTING_SMS_ALERT_NAME")
        self.SKY_LOG_ALERTING_BASE_URL = config("SKY_LOG_ALERTING_BASE_URL")
        self.SKY_LOG_ALERTING_TOKEN = config("SKY_LOG_ALERTING_TOKEN")


class LazySettings:
    _wrapped = None

    def _setup(self):
        if self._wrapped is None:
            setting = dataclasses.dataclass(ClientSettings)()
            setting._setup()
            self._wrapped = setting
        return self._wrapped

    def __getattr__(self, item):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, item)


settings = LazySettings()
