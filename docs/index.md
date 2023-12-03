# skylog-sdk

[![Release](https://img.shields.io/github/v/release/vahidtwo/skylog-sdk)](https://img.shields.io/github/v/release/vahidtwo/skylog-sdk)
[![Build status](https://img.shields.io/github/actions/workflow/status/vahidtwo/skylog-sdk/main.yml?branch=main)](https://github.com/vahidtwo/skylog-sdk/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/vahidtwo/skylog-sdk)](https://img.shields.io/github/commit-activity/m/vahidtwo/skylog-sdk)
[![License](https://img.shields.io/github/license/vahidtwo/skylog-sdk)](https://img.shields.io/github/license/vahidtwo/skylog-sdk)

- **Github repository**: <https://github.com/vahidtwo/skylog-sdk/>
- **Documentation** <https://vahidtwo.github.io/skylog-sdk/>

# Python SDK for Skylog Integration

Skylog is a robust service designed for seamless integration with various platforms like Sentry, Telegram,
and more, enabling the efficient transmission of logs and rapid identification of issues.

This Python SDK facilitates easy interaction with Skylog services, allowing users to:

- fire alert
- stop alert
- notify

# How to install

install from gitlab

```bash
pip install skylog-sdk
```

## Setup and Configuration

- **Environment Variables**: Configure the following variables in your project environment:

  - `DEFAULT_SKY_LOG_ALERTING_TELEGRAM_ALERT_NAME`: Default alert name for Telegram
  - `DEFAULT_SKY_LOG_ALERTING_PHONE_CALL_ALERT_NAME`: Default alert name for phone calls
  - `DEFAULT_SKY_LOG_ALERTING_SMS_ALERT_NAME`: Default alert name for SMS
  - `SKY_LOG_BASE_URL`: Base URL for Skylog API calls
  - `SKY_LOG_ALERTING_TOKEN`: Your Skylog authentication token

- **Proxy Configuration**: If using a proxy, include the following additional variables:
  - `PROXY_USERNAME`
  - `PROXY_PASSWORD`
  - `PROXY_IP`
  - `PROXY_PORT`

## Usage Example

```python
from skylog import AlertingSkyLogClient, AlertingProvider

# Initialize the Skylog client with the desired provider (e.g., Telegram)
client = AlertingSkyLogClient(provider=AlertingProvider.telegram)

# Example Operations:
client.fire_alert(description='Issue detected', instance_name='unique_key', provider=AlertingProvider.sms)
client.stop_alert(description='Issue resolved', instance_name='unique_key', provider=AlertingProvider.sms)
client.notify(description='Alert notification', instance_name='unique_key', provider=AlertingProvider.telegram)
```

## Concepts to Understand

### Alertname and Instance

- **Alertname**: Represents the provider or service. It identifies where Skylog sends alerts.
- **Instance**: A unique identifier within a group alert, specifying a particular part of a universal alert.

### Alerts Management

- **Firing an Alert**: Triggering an alert, resulting in immediate notifications sent to relevant endpoints.
- **Stopping an Alert**: Removing a fired alert, resolving it and stopping further notifications.
- **Notifying an Alert**: Sending messages to endpoints without adding records to the triggered list.
