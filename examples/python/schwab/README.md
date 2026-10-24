# Python alerts to Charles Schwab

To place orders at Charles Schwab from a Python script, create a Nyria strategy with Custom webhook as the alert source, connect your Charles Schwab account, and `POST` a JSON body to the strategy's webhook URL with `requests`. The body names a ticker, a side and an action. Nyria places the order in your Charles Schwab account. Your script needs no broker SDK and no keys beyond the webhook URL.

## What you need

- Python 3 and `requests`.
- A free Nyria account and your Charles Schwab account. Test on paper first; live trading is from $15 a month.

## How do I set up Python alerts to Schwab?

1. Connect Schwab. In Nyria, select Integrations, then the Charles Schwab card, then Connect live account. Sign in at schwab.com and select Allow on the Authorize App screen. No developer account or API key is needed. Schwab ends Nyria's access every 7 days. Select Reconnect live account and sign in again each week.
2. Create a strategy. Select Create strategy and pick Custom webhook as the alert source. Choose stocks or options as the asset type, and set what an entry and an exit do on each side.
3. Copy the webhook URL from the strategy's Integration tab. It has the form `https://trades.nyria.io/webhooks/<your-strategy-token>`. Keep it in an environment variable and out of the repository.
4. Send a body from the list below with an HTTPS `POST`. JSON goes as `application/json` and a line of text as `text/plain`.
5. Back in Nyria, select Check format on the strategy, then Check and save. The strategy turns Active once Nyria reads every side, and the Logs tab shows the ticker, side and contract it read.
6. Deploy a bot. Select Deploy bot, pick the Schwab account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. Schwab has no paper account to connect. Run the strategy on Nyria Paper first, then deploy a second bot on the Schwab account.

## What must the alert say?

Nyria needs three things from an alert: a ticker, a direction (long or short) and an action (open or close). There is no fixed template. The keys `ticker`, `instrument` and `symbol` mean the same thing. `action` is `OPEN` or `CLOSE`, and `buy` and `sell` also work. Send `direction` with `OPEN` and `CLOSE` to state the side outright.

## Alert messages

Each message below is a file in this folder and is read back by Nyria's alert tester through [`scripts/check_examples.py`](../../../scripts/check_examples.py). The ticker and sample values are placeholders; use your own.

A script that sends one of these files: [`../send_alert.py`](../send_alert.py).

```python
import os
import requests

url = os.environ["NYRIA_WEBHOOK_URL"]  # https://trades.nyria.io/webhooks/<your-strategy-token>
alert = {"ticker": "AAPL", "action": "OPEN", "direction": "LONG"}

response = requests.post(url, json=alert, timeout=10)
body = response.json()
print(response.status_code, body)
assert body.get("status") == "processed"  # a 200 can also carry "rejected" or "duplicate"
```

### Stocks and ETFs

**Long entry at market.** Buys to open AAPL at market.

```json
{
  "ticker": "AAPL",
  "action": "OPEN",
  "direction": "LONG",
  "order_type": "market"
}
```

File: [`stock-open-long.json`](stock-open-long.json)

**Long exit.** Closes the whole AAPL long. There is no partial-close field.

```json
{
  "ticker": "AAPL",
  "action": "CLOSE",
  "direction": "LONG"
}
```

File: [`stock-close-long.json`](stock-close-long.json)

### Options

**Single call, contract in the alert.** For a strategy set to Provided in alert. Buys to open the SPY 780 call that expires 2026-12-18.

```json
{
  "ticker": "SPY",
  "action": "OPEN",
  "direction": "LONG",
  "legs": [
    {
      "side": "CALL",
      "strike": 780,
      "expiration": "2026-12-18",
      "action": "buy_to_open"
    }
  ]
}
```

File: [`option-call-by-legs.json`](option-call-by-legs.json)

**Close that call.** Sells to close the SPY 780 call.

```json
{
  "ticker": "SPY",
  "action": "CLOSE",
  "direction": "LONG",
  "legs": [
    {
      "side": "CALL",
      "strike": 780,
      "expiration": "2026-12-18",
      "action": "sell_to_close"
    }
  ]
}
```

File: [`option-call-close.json`](option-call-close.json)

## How do options alerts work at Schwab?

Schwab takes options as single legs or spreads of up to 4 legs, sent as one order, all on one expiration. With contract selection set to Provided in alert, send a `legs` array with one entry per leg: `side` (`CALL` or `PUT`), `strike`, `expiration` as `YYYY-MM-DD`, and `action` (`buy_to_open`, `sell_to_open`, `buy_to_close` or `sell_to_close`). With From my rules, send no `legs` and the strategy's leg rules pick the contract. Calendars, diagonals and ratio spreads cannot be built, because every leg shares one expiration and one quantity. Change the strikes and the expiration in these files to a contract that exists on the day you use them.

## Can I trade crypto at Schwab?

No. Schwab's API does not offer crypto, so a crypto alert places no order at Schwab. Use Alpaca or Nyria Paper for crypto. See the [Alpaca folder](../alpaca/README.md) and the [Nyria Paper folder](../nyria-paper/README.md) for crypto spot.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Be read twice.** The same body again within 30 seconds, or within 5 minutes with nothing else in between, is dropped as a duplicate. Add a unique `metadata.message_id` to scale in.
- **Trade crypto at Schwab.** Schwab does not carry crypto through Nyria. Use Alpaca or Nyria Paper.

## Charles Schwab notes

- Live accounts only, connected through Schwab's own sign-in. Nyria's token places and cancels orders and cannot move money.
- Stocks in whole shares and options in whole contracts. Nyria enters whole shares, so Schwab Stock Slices are not used for entries.
- Market and limit orders. A spread goes as one order for all its legs, priced as a net debit or credit when it is a limit order.
- The strategy's Duration goes to Schwab as set: Day, Good till canceled or Fill or kill.
- Schwab needs options approval at the level the trade requires. Spreads need a higher level than buying calls or puts.
- Short stock and short spreads need a margin account.
- Schwab's API does not offer crypto, so a crypto alert places no order at Schwab. Use Alpaca or Nyria Paper for crypto.
- MODIFY is refused at Schwab. To re-price a resting entry, send CANCEL, then a new OPEN.

## Links

- [How to automate webhook alerts to Charles Schwab](https://nyria.io/automate/webhook-to-schwab): the step-by-step page on nyria.io
- [Python on Nyria](https://nyria.io/signals/webhooks)
- [Guide: Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Charles Schwab on Nyria](https://nyria.io/integrations/schwab) and [the Charles Schwab docs](https://docs.nyria.io/integrations/brokers/schwab)
- [Python setup in the docs](https://docs.nyria.io/alerts/custom-webhook)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
