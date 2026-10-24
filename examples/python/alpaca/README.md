# Python alerts to Alpaca

To place orders at Alpaca from a Python script, create a Nyria strategy with Custom webhook as the alert source, connect your Alpaca account, and `POST` a JSON body to the strategy's webhook URL with `requests`. The body names a ticker, a side and an action. Nyria places the order in your Alpaca account. Your script needs no broker SDK and no keys beyond the webhook URL.

## What you need

- Python 3 and `requests`.
- A free Nyria account and your Alpaca account. Test on paper first; live trading is from $15 a month.

## How do I set up Python alerts to Alpaca?

1. Connect Alpaca. In the Alpaca dashboard, switch to Paper or Live and select Generate New Keys. Copy the API key ID and the secret key; Alpaca shows the secret once. Give the key trading permission only. In Nyria, select Integrations, then the Alpaca card, then Connect paper account or Connect live account. Select Accept and continue and paste both values. A paper key works only on paper and a live key only on live, so the same strategy can run on both.
2. Create a strategy. Select Create strategy and pick Custom webhook as the alert source. Choose stocks, options or crypto as the asset type, and set what an entry and an exit do on each side.
3. Copy the webhook URL from the strategy's Integration tab. It has the form `https://trades.nyria.io/webhooks/<your-strategy-token>`. Keep it in an environment variable and out of the repository.
4. Send a body from the list below with an HTTPS `POST`. JSON goes as `application/json` and a line of text as `text/plain`.
5. Back in Nyria, select Check format on the strategy, then Check and save. The strategy turns Active once Nyria reads every side, and the Logs tab shows the ticker, side and contract it read.
6. Deploy a bot. Select Deploy bot, pick the Alpaca account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. An Alpaca paper account connects the same way as a live one, and Nyria Paper works too.

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

### Crypto

**Crypto entry.** Buys BTCUSD spot, sized from the bot's budget.

```json
{
  "ticker": "BTCUSD",
  "action": "OPEN",
  "direction": "LONG"
}
```

File: [`crypto-open-long.json`](crypto-open-long.json)

**Crypto exit.** Sells the BTCUSD position.

```json
{
  "ticker": "BTCUSD",
  "action": "CLOSE",
  "direction": "LONG"
}
```

File: [`crypto-close-long.json`](crypto-close-long.json)

## How do options alerts work at Alpaca?

Alpaca takes options as single legs or spreads of up to 4 legs, sent as one order, all on one expiration. With contract selection set to Provided in alert, send a `legs` array with one entry per leg: `side` (`CALL` or `PUT`), `strike`, `expiration` as `YYYY-MM-DD`, and `action` (`buy_to_open`, `sell_to_open`, `buy_to_close` or `sell_to_close`). With From my rules, send no `legs` and the strategy's leg rules pick the contract. Calendars, diagonals and ratio spreads cannot be built, because every leg shares one expiration and one quantity. Change the strikes and the expiration in these files to a contract that exists on the day you use them.

## Can I trade crypto at Alpaca?

Alpaca trades crypto spot in the pairs it lists. Crypto orders go to Alpaca as good till canceled, and positions are fractional. Use a strategy whose asset type is crypto. A short form such as `BTC` or `BTCUSD` works while only one selected pair matches it; if you select both the USDT and the USDC pair for a coin, the alert must name the full pair.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Be read twice.** The same body again within 30 seconds, or within 5 minutes with nothing else in between, is dropped as a duplicate. Add a unique `metadata.message_id` to scale in.

## Alpaca notes

- Alpaca connects with an API key, not a sign-in. Nyria stores the key encrypted at rest.
- Stocks, options up to 4 legs and crypto spot. Options trading must be turned on in the Alpaca account.
- Market and limit orders. Stock orders take the strategy's Duration as set. Option orders go to Alpaca as Day, and crypto orders as Good till canceled.
- Stocks in whole shares. Crypto trades in fractions, so a $100 entry with BTC at $64,000 buys 0.00156 BTC.
- US equities only. Alpaca restricts some order types outside market hours; turn on Limit trading hours on the strategy to keep entries inside them.
- MODIFY works at Alpaca, so a resting limit entry can be re-priced with a second alert.

## Links

- [How to automate webhook alerts to Alpaca](https://nyria.io/automate/webhook-to-alpaca): the step-by-step page on nyria.io
- [Python on Nyria](https://nyria.io/signals/webhooks)
- [Guide: Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Alpaca on Nyria](https://nyria.io/integrations/alpaca) and [the Alpaca docs](https://docs.nyria.io/integrations/brokers/alpaca)
- [Python setup in the docs](https://docs.nyria.io/alerts/custom-webhook)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
