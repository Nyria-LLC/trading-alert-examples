# Webhook

Post an alert from your own code to a Nyria strategy. Any program that can make an HTTPS request can do it.

1. In Nyria, create a strategy with Custom webhook as the alert source and open its Integration tab.
2. Copy the webhook URL. It has the form `https://trades.nyria.io/webhooks/<your-strategy-token>`.
3. Put it in an environment variable. Do not commit it.

```sh
export NYRIA_WEBHOOK_URL='https://trades.nyria.io/webhooks/<your-strategy-token>'
```

The token in the path is the endpoint's only authentication: there is no Authorization header, no signature and no IP allowlist. Treat the URL like an API key. If it leaks, select Rotate token on the Integration tab; the old URL stops working at once.

Check a payload in the [alert tester](https://nyria.io/tools/alert-tester) before the first real post, and deploy the first bot on Nyria Paper.

## Senders

| File | Needs | Run |
|---|---|---|
| [`send_alert.sh`](send_alert.sh) | curl 7.76+ | `./send_alert.sh [payload.json]` |
| [`send_alert.py`](send_alert.py) | Python 3 and `requests` | `python3 send_alert.py [payload.json]` |
| [`send_alert.mjs`](send_alert.mjs) | Node 18+ | `node send_alert.mjs [payload.json]` |

Each reads `NYRIA_WEBHOOK_URL` and posts a file from [`payloads/`](payloads), `stock-open-long.json` by default. The Python and Node senders exit with status 0 only when the answer is `{"status": "processed"}`.

The same request by hand:

```sh
curl -X POST "$NYRIA_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{ "ticker": "AAPL", "action": "OPEN", "direction": "LONG", "order_type": "market" }'
```

A line of text works too, sent as `text/plain`:

```sh
curl -X POST "$NYRIA_WEBHOOK_URL" \
  -H "Content-Type: text/plain" \
  -d 'SPY long entry'
```

## Payloads

Every file in [`payloads/`](payloads) is read back by the alert tester through [`../scripts/check_examples.py`](../scripts/check_examples.py).

| File | Reads as |
|---|---|
| [`stock-open-long.json`](payloads/stock-open-long.json) | Buy to open AAPL at market |
| [`stock-close-long.json`](payloads/stock-close-long.json) | Close the AAPL long |
| [`stock-open-short.json`](payloads/stock-open-short.json) | Sell to open an AAPL short |
| [`stock-open-limit.json`](payloads/stock-open-limit.json) | Buy to open SPY with a limit price |
| [`crypto-open-long.json`](payloads/crypto-open-long.json) | Buy BTCUSD spot |
| [`option-by-rules.json`](payloads/option-by-rules.json) | Open a long SPY option; the strategy's leg rules pick the contract |
| [`option-call-by-legs.json`](payloads/option-call-by-legs.json) | Buy to open the SPY 780 call that expires 2026-12-18 |
| [`option-call-close.json`](payloads/option-call-close.json) | Sell to close that call |
| [`option-call-spread.json`](payloads/option-call-spread.json) | A call vertical: buy the 780 call, sell the 785 call |

The two `legs` payloads need a strategy whose contract selection is "Provided in alert". `option-by-rules.json` needs "From my rules". Change the strikes and the expiration to a contract that exists on the day you use them; the checker fails an example whose date has passed.

Fields:

| Field | Meaning |
|---|---|
| `ticker`, `instrument`, `symbol` | The ticker. All three keys mean the same thing. |
| `action` | `OPEN` or `CLOSE` for entries and exits. `MODIFY` and `CANCEL` manage a working order. |
| `direction` | `LONG` or `SHORT`. Send it with `OPEN` and `CLOSE`. |
| `order_type` | `market` or `limit`. Read on alerts that name `action` and `direction`. |
| `price` | The limit price, with `order_type` `limit`. |
| `legs` | Option legs: `side`, `strike`, `expiration`, `action` (`buy_to_open`, `sell_to_open`, `buy_to_close`, `sell_to_close`). |
| `metadata.message_id` | A value Nyria compares to spot duplicates instead of hashing the whole body. |

An alert cannot set the entry size; Nyria ignores a `quantity` or `notional` key on an entry. Size comes from the bot's budget per entry. Nyria places market and limit orders only.

## Reading the answer

| Answer | Meaning |
|---|---|
| `200`, `"status": "processed"` | Nyria read the alert and handed it to the bots. This is not a fill; the bot's Logs tab shows what the broker did. |
| `200`, `"status": "rejected"` or `"rejected": true` | The strategy is not Active (draft, paused or archived), the ticker is not in its list, that direction is off, or there is no open position to close. |
| `200`, `"status": "duplicate"` | The body repeats an earlier one: identical within 30 seconds, or within 5 minutes with nothing else in between. |
| `400` or `404` | The token in the URL is malformed or belongs to no strategy. |
| `413` | The payload is larger than 256 KB. |
| `422` | Nyria could not use the alert. `userMessage` names the cause. |
| `429` | More than 10 alerts at once, then 1 a second. Wait as long as `Retry-After` says, then resend. |
| `503` | Reading the alert or fetching market data failed temporarily. Sending the same alert again can succeed. |

To send the same body twice on purpose, make the bodies differ, or set a unique `metadata.message_id` on each.

## Links

- [Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [Send alerts from your own bot](https://docs.nyria.io/alerts/custom-webhook)
- [Webhook alerts to your broker](https://nyria.io/signals/webhooks)
