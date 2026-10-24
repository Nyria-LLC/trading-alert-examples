# Python alerts to a broker

Send an alert from a Python script to a Nyria strategy, and a bot places the order at Charles Schwab, Tradier, tastytrade, Alpaca or on Nyria Paper, the free simulated broker. The script needs `requests` and the strategy's webhook URL. It holds no broker keys and imports no broker SDK.

## Pick your broker

| Broker | Payloads and setup |
|---|---|
| Charles Schwab | [Python alerts to Charles Schwab](schwab/README.md) |
| Tradier | [Python alerts to Tradier](tradier/README.md) |
| tastytrade | [Python alerts to tastytrade](tastytrade/README.md) |
| Alpaca | [Python alerts to Alpaca](alpaca/README.md), with crypto |
| Nyria Paper | [Python alerts to Nyria Paper](nyria-paper/README.md), with crypto |

The payload does not change with the broker. Nyria turns it into that broker's order format.

## How do I send an alert from Python?

1. In Nyria, create a strategy with Custom webhook as the alert source and copy the webhook URL from its Integration tab.
2. Export it: `export NYRIA_WEBHOOK_URL='https://trades.nyria.io/webhooks/<your-strategy-token>'`. The token is the only authentication, so keep it out of the repository.
3. Run the sender with a payload file:

```sh
python3 send_alert.py schwab/stock-open-long.json
```

[`send_alert.py`](send_alert.py) posts the file and exits with status 0 only when Nyria answers `{"status": "processed"}`. A `200` can also carry a rejection or a duplicate, so the script checks the body as well as the status code. A `200` means Nyria read the alert and handed it to the bots; it does not mean the broker filled it.

Inline, the same thing is:

```python
import os
import requests

url = os.environ["NYRIA_WEBHOOK_URL"]
alert = {"ticker": "AAPL", "action": "OPEN", "direction": "LONG"}

response = requests.post(url, json=alert, timeout=10)
print(response.status_code, response.json())
```

Always set a timeout. `raise_for_status()` catches 4xx and 5xx but not a rejection or a duplicate, which answer `200`, so check `status` too. On `429`, wait as long as the `Retry-After` header says. On `503`, sending the same alert again can succeed.

## Links

- [Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [The webhook folder](../webhook/README.md): more payloads, curl and Node senders, and the full table of answers.
