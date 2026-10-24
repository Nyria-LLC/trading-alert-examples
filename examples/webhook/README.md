# Webhook alerts to a broker

Post an alert from your own code to a Nyria strategy, and a bot places the order at Charles Schwab, Tradier, tastytrade, Alpaca or on Nyria Paper, the free simulated broker. Any program that can make an HTTPS request can do it: curl, Node, Go, a cron job, a spreadsheet script.

## Pick your broker

| Broker | Payloads and setup |
|---|---|
| Charles Schwab | [Webhook alerts to Charles Schwab](schwab/README.md) |
| Tradier | [Webhook alerts to Tradier](tradier/README.md) |
| tastytrade | [Webhook alerts to tastytrade](tastytrade/README.md) |
| Alpaca | [Webhook alerts to Alpaca](alpaca/README.md), with crypto |
| Nyria Paper | [Webhook alerts to Nyria Paper](nyria-paper/README.md), with crypto |

The payload does not change with the broker. Nyria turns it into that broker's order format. Python scripts have their own folder: [Python](../python/README.md).

## How do I send the first alert?

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
| [`send_alert.sh`](send_alert.sh) | curl 7.76+ | `./send_alert.sh schwab/stock-open-long.json` |
| [`send_alert.mjs`](send_alert.mjs) | Node 18+ | `node send_alert.mjs schwab/stock-open-long.json` |
| [`../python/send_alert.py`](../python/send_alert.py) | Python 3 and `requests` | `python3 ../python/send_alert.py schwab/stock-open-long.json` |

Each reads `NYRIA_WEBHOOK_URL`. The Python and Node senders exit with status 0 only when the answer is `{"status": "processed"}`. A `.txt` file goes as `text/plain` and anything else as `application/json`.

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
  -d 'AAPL long entry'
```

## Which fields does a payload take?

| Field | Meaning |
|---|---|
| `ticker`, `instrument`, `symbol` | The ticker. All three keys mean the same thing. |
| `action` | `OPEN` or `CLOSE` for entries and exits. `MODIFY` and `CANCEL` manage a working order. `buy`, `sell`, `entry` and `exit` also work. |
| `direction` | `LONG` or `SHORT`. Send it with `OPEN` and `CLOSE`. |
| `order_type` | `market` or `limit`. Read on alerts that name `action` and `direction`. |
| `price` | The limit price, with `order_type` `limit`. For a multi-leg order, the net price. |
| `marketPosition`, `prevMarketPosition` | TradingView's position before and after a fill. Send both and Nyria works out the action and direction. |
| `legs` | Option legs: `side`, `strike`, `expiration`, `action` (`buy_to_open`, `sell_to_open`, `buy_to_close`, `sell_to_close`). Up to 4, all on one expiration. |
| `metadata.message_id` | A value Nyria compares to spot duplicates instead of hashing the whole body. |

An alert cannot set the entry size; Nyria ignores a `quantity` or `notional` key on an entry. Size comes from the bot's budget. Nyria places market and limit orders only.

`MODIFY` re-prices a resting limit order and works at Tradier and Alpaca. `CANCEL` pulls a resting entry. Schwab and tastytrade refuse `MODIFY`, so send `CANCEL` and a new `OPEN` there. Both are described in the [webhook reference](https://docs.nyria.io/webhook-reference) and are not part of the tester-checked set in this repository.

## What does the answer mean?

| Answer | Meaning |
|---|---|
| `200`, `"status": "processed"` | Nyria read the alert and handed it to the bots. This is not a fill; the bot's Logs tab shows what the broker did. |
| `200`, `"status": "rejected"` or `"rejected": true` | The strategy is not Active (draft, paused or archived), the ticker is not in its list, that direction is off, or there is no open position to close. |
| `200`, `"status": "duplicate"` | The body repeats an earlier one: identical within 30 seconds, or within 5 minutes with nothing else in between. |
| `400` or `404` | The body is empty or the token in the URL is malformed, or it belongs to no strategy. |
| `413` | The payload is larger than 256 KB. |
| `422` | Nyria could not use the alert. `userMessage` names the cause. |
| `429` | More than 10 alerts at once, then 1 a second. Wait as long as `Retry-After` says, then resend. |
| `503` | Reading the alert or fetching market data failed temporarily. Sending the same alert again can succeed. |

To send the same body twice on purpose, make the bodies differ, or set a unique `metadata.message_id` on each. See `scale-in-message-id.json` in any broker folder.

## Links

- [Webhook alerts to your broker](https://nyria.io/signals/webhooks)
- [Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [Send alerts from your own bot](https://docs.nyria.io/alerts/custom-webhook)
