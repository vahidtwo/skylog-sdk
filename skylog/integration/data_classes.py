import dataclasses


@dataclasses.dataclass
class AlertingProvider:
    telegram: str
    phone_call: str
    sms: str
