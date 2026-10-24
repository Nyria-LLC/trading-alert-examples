# trading-alert-examples

Copy-pasteable alert messages for [Nyria](https://nyria.io): how to automate TradingView alerts to Charles Schwab, Tradier, tastytrade and Alpaca, and how to send the same orders from TrendSpider, Discord, Telegram, Python or any webhook.

**How do I automate TradingView alerts to a broker?** Create a strategy in Nyria with TradingView as the alert source, connect your Charles Schwab, Tradier, tastytrade or Alpaca account (or the free Nyria Paper simulator), and paste the strategy's webhook URL into the alert's Webhook URL box. The alert message names a ticker, a side and whether it opens or closes a position. Nyria reads it and a bot places the order in your own account. TradingView needs a paid plan with two-factor sign-in on to send webhooks. An alert cannot set the size of an order or attach a stop, and live trading is from $15 a month.

Every alert in this repository is listed in [`alerts.json`](alerts.json) and run through Nyria's public [alert tester](https://nyria.io/tools/alert-tester) by [`scripts/check_examples.py`](scripts/check_examples.py), so each one is read the way this page says it is.

## Questions answered

- [How do I automate TradingView alerts to a broker?](#quick-start)
- [How do I automate TradingView alerts to Charles Schwab, Tradier, tastytrade, Alpaca or Nyria Paper?](#tradingview-alerts-to-each-broker)
- [How do I send alerts from TrendSpider, Discord, Telegram, Python or a custom webhook?](#alert-sources)
- [Can alerts trade options and multi-leg spreads?](#options-single-and-multi-leg)
- [Can alerts trade crypto?](#crypto)
- [How is an alert read, and what can it not do?](#how-an-alert-is-read)
- [How do I check an alert before it trades?](#check-an-alert-before-it-fires)
- [Short answers to common questions](FAQ.md)

## Quick start

1. Create a free Nyria account and a strategy with TradingView as the alert source (My strategies, Create strategy).
2. Open the strategy's Integration tab and copy the webhook URL. It looks like `https://trades.nyria.io/webhooks/<your-strategy-token>`.
3. In TradingView (paid plan, two-factor sign-in on) press Alt+A on a chart. Set Condition to your strategy with "Order fills only", paste this into Message, tick "Webhook URL" under Notifications and paste the URL:

```json
{
  "action": "{{strategy.order.action}}",
  "instrument": "{{ticker}}",
  "marketPosition": "{{strategy.market_position}}",
  "prevMarketPosition": "{{strategy.prev_market_position}}",
  "contracts": "{{strategy.order.contracts}}",
  "price": {{close}}
}
```

4. Back in Nyria, select Check format, then deploy a bot on Nyria Paper and let the alert fire. The order shows on the bot's Logs tab, where you can hold it up against the alert that caused it.

Using an indicator instead of a strategy, a stock, option or crypto alert, or no TradingView at all? Read on.

## TradingView alerts to each broker

The alert message is the same for every broker. The bot you deploy decides where the order goes. What differs is how the broker connects and what it supports.

| Broker | Connects with | Stocks | Options | Crypto spot | Paper |
|---|---|---|---|---|---|
| Charles Schwab | Schwab sign-in, reconnect every 7 days | yes | up to 4 legs | no | no, use Nyria Paper |
| Tradier | Tradier sign-in, or sandbox credentials | yes | up to 4 legs | no | Tradier Sandbox |
| tastytrade | tastytrade sign-in | yes | up to 4 legs | no, disabled in its API | no, use Nyria Paper |
| Alpaca | API key | yes | up to 4 legs | yes | Alpaca paper account |
| Nyria Paper | nothing to connect | yes | up to 4 legs | yes | free simulated broker |

### TradingView alerts to Charles Schwab

To automate TradingView alerts to Charles Schwab, connect Schwab in Nyria, create a strategy with TradingView as the alert source, and paste the strategy's webhook URL into the alert. Each alert becomes an order in your Charles Schwab account.

Steps:

1. In Nyria, select Integrations, then the Charles Schwab card, then Connect live account.
2. Create a strategy with TradingView as the alert source and open its Integration tab.
3. In TradingView (paid plan, two-factor sign-in on) press Alt+A, paste a message below, tick Webhook URL under Notifications and paste `https://trades.nyria.io/webhooks/<your-strategy-token>`.
4. Select Check format in Nyria, deploy a bot on Nyria Paper first, then on the live account.

Entry from an indicator:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

The matching exit, a second alert on the same indicator:

```json
{
  "action": "CLOSE",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

The alert must say a ticker, a side and whether it opens or closes. It cannot set the size, because each bot sizes the order from its own budget per entry, and it cannot attach a stop or target, because Nyria sends market and limit orders only.

Schwab ends Nyria's access every 7 days, so reconnect weekly. Schwab has no paper account, so test on Nyria Paper first. It does not carry crypto through Nyria.

More: [TradingView alerts to Charles Schwab on nyria.io](https://nyria.io/automate/tradingview-to-schwab), [the Charles Schwab folder](examples/tradingview/schwab/README.md) with every message, and the same alert from [TrendSpider](examples/trendspider/schwab/README.md), [Discord](examples/discord/schwab/README.md), [Telegram](examples/telegram/schwab/README.md) and [Python](examples/python/schwab/README.md).

### TradingView alerts to Tradier

To automate TradingView alerts to Tradier, connect Tradier in Nyria, create a strategy with TradingView as the alert source, and paste the strategy's webhook URL into the alert. Each alert becomes an order in your Tradier account.

Steps:

1. In Nyria, select Integrations, then the Tradier card, then Connect live account, and approve access on Tradier's own screen.
2. Create a strategy with TradingView as the alert source and open its Integration tab.
3. In TradingView (paid plan, two-factor sign-in on) press Alt+A, paste a message below, tick Webhook URL under Notifications and paste `https://trades.nyria.io/webhooks/<your-strategy-token>`.
4. Select Check format in Nyria, deploy a bot on Nyria Paper first, then on the live account.

A limit entry at the bar close:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG",
  "order_type": "limit",
  "price": {{close}}
}
```

A strategy alert as a plain sentence:

```text
{{strategy.order.action}} {{ticker}} @ {{close}}
```

The alert must say a ticker, a side and whether it opens or closes. It cannot set the size, because each bot sizes the order from its own budget per entry, and it cannot attach a stop or target, because Nyria sends market and limit orders only.

Tradier's sandbox connects as a paper account. Fill or kill goes as Day, `MODIFY` works, and there is no crypto.

More: [TradingView alerts to Tradier on nyria.io](https://nyria.io/automate/tradingview-to-tradier), [the Tradier folder](examples/tradingview/tradier/README.md) with every message, and the same alert from [TrendSpider](examples/trendspider/tradier/README.md), [Discord](examples/discord/tradier/README.md), [Telegram](examples/telegram/tradier/README.md) and [Python](examples/python/tradier/README.md).

### TradingView alerts to tastytrade

To automate TradingView alerts to tastytrade, connect tastytrade in Nyria, create a strategy with TradingView as the alert source, and paste the strategy's webhook URL into the alert. Each alert becomes an order in your tastytrade account.

Steps:

1. In Nyria, select Integrations, then the tastytrade card. Under Live trading select Connect live account.
2. Create a strategy with TradingView as the alert source and open its Integration tab.
3. In TradingView (paid plan, two-factor sign-in on) press Alt+A, paste a message below, tick Webhook URL under Notifications and paste `https://trades.nyria.io/webhooks/<your-strategy-token>`.
4. Select Check format in Nyria, deploy a bot on Nyria Paper first, then on the live account.

An options entry. The strategy's leg rules pick the contract:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

A multi-leg entry at a net price:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG",
  "order_type": "limit",
  "price": 1.50
}
```

The alert must say a ticker, a side and whether it opens or closes. It cannot set the size, because each bot sizes the order from its own budget per entry, and it cannot attach a stop or target, because Nyria sends market and limit orders only.

tastytrade connects live accounts only. Defined-risk spreads need options level 3 or higher. Crypto has been disabled through its API since 29 June 2026.

More: [TradingView alerts to tastytrade on nyria.io](https://nyria.io/automate/tradingview-to-tastytrade), [the tastytrade folder](examples/tradingview/tastytrade/README.md) with every message, and the same alert from [TrendSpider](examples/trendspider/tastytrade/README.md), [Discord](examples/discord/tastytrade/README.md), [Telegram](examples/telegram/tastytrade/README.md) and [Python](examples/python/tastytrade/README.md).

### TradingView alerts to Alpaca

To automate TradingView alerts to Alpaca, connect Alpaca in Nyria, create a strategy with TradingView as the alert source, and paste the strategy's webhook URL into the alert. Each alert becomes an order in your Alpaca account.

Steps:

1. In the Alpaca dashboard, switch to Paper or Live and select Generate New Keys. Copy the API key ID and the secret key; Alpaca shows the secret once. Give the key trading permission only.
2. Create a strategy with TradingView as the alert source and open its Integration tab.
3. In TradingView (paid plan, two-factor sign-in on) press Alt+A, paste a message below, tick Webhook URL under Notifications and paste `https://trades.nyria.io/webhooks/<your-strategy-token>`.
4. Select Check format in Nyria, deploy a bot on Nyria Paper first, then on the live account.

A crypto entry on a crypto chart:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

The crypto exit:

```json
{
  "action": "CLOSE",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

The alert must say a ticker, a side and whether it opens or closes. It cannot set the size, because each bot sizes the order from its own budget per entry, and it cannot attach a stop or target, because Nyria sends market and limit orders only.

Alpaca connects with an API key, paper or live. It carries crypto spot, and `MODIFY` works. Option orders go as Day and crypto orders as Good till canceled.

More: [TradingView alerts to Alpaca on nyria.io](https://nyria.io/automate/tradingview-to-alpaca), [the Alpaca folder](examples/tradingview/alpaca/README.md) with every message, and the same alert from [TrendSpider](examples/trendspider/alpaca/README.md), [Discord](examples/discord/alpaca/README.md), [Telegram](examples/telegram/alpaca/README.md) and [Python](examples/python/alpaca/README.md).

### TradingView alerts to Nyria Paper

To test TradingView alerts without a broker, connect Nyria Paper, point a strategy's webhook at it and deploy a paper bot. Orders are simulated against the live quote, nothing reaches a real broker, and the bot's Logs tab shows each fill beside the alert that caused it.

Steps:

1. Create the Nyria Paper account under Integrations. It needs no broker or card.
2. Create a strategy with TradingView as the alert source and open its Integration tab.
3. In TradingView (paid plan, two-factor sign-in on) press Alt+A, paste a message below, tick Webhook URL under Notifications and paste `https://trades.nyria.io/webhooks/<your-strategy-token>`.
4. Select Check format in Nyria and deploy a paper bot. The next alert becomes a simulated order.

One alert for every fill of a strategy:

```json
{
  "action": "{{strategy.order.action}}",
  "instrument": "{{ticker}}",
  "marketPosition": "{{strategy.market_position}}",
  "prevMarketPosition": "{{strategy.prev_market_position}}",
  "contracts": "{{strategy.order.contracts}}",
  "price": {{close}}
}
```

A short entry from an indicator:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "SHORT"
}
```

The alert must say a ticker, a side and whether it opens or closes. It cannot set the size, because each bot sizes the order from its own budget per entry, and it cannot attach a stop or target, because Nyria sends market and limit orders only.

Up to 10 paper bots run without a plan. Options alerts are refused while the options market is closed, and there is no slippage, so paper fills usually read better than live ones.

More: [TradingView alerts to Nyria Paper on nyria.io](https://nyria.io/automate/tradingview-to-paper), [the Nyria Paper folder](examples/tradingview/nyria-paper/README.md) with every message, and the same alert from [TrendSpider](examples/trendspider/nyria-paper/README.md), [Discord](examples/discord/nyria-paper/README.md), [Telegram](examples/telegram/nyria-paper/README.md) and [Python](examples/python/nyria-paper/README.md).

## Alert sources

A strategy reads alerts from one source. Each source has a folder per broker under [`examples/`](examples/README.md).

### TradingView alerts

Paid TradingView plan with two-factor sign-in, a webhook URL in the alert's Notifications, and a message that names the side. A `strategy()` needs one Order-fills alert per ticker. An `indicator()` needs one alert per side. Two Pine Script v6 examples build the message in code: [`indicator_alert.pine`](examples/tradingview/pine/indicator_alert.pine) and [`strategy_alert_message.pine`](examples/tradingview/pine/strategy_alert_message.pine). More: [examples/tradingview](examples/tradingview/README.md).

### TrendSpider alerts

TrendSpider has no action variable, so write the action into each alert and leave quantity out. Paste this into the alert's note:

```json
{
  "symbol": "%alert_symbol%",
  "action": "buy",
  "price": "%last_price%"
}
```

Account-level Alerts share one webhook URL and feed one Nyria strategy. Strategy Bots each have their own URL, use `%bot_symbol%` and can feed different strategies. More: [examples/trendspider](examples/trendspider/README.md).

### Discord alerts

Nyria reads one channel of a server you run. Post the call the way a trader would:

```text
SPY long entry
BTO SPY 12/18 780C
Close SPY long
```

More: [examples/discord](examples/discord/README.md).

### Telegram alerts

Nyria reads one group or channel you run, as an admin that only reads. The same lines work:

```text
long SPY here
STC SPY 780c 12/18
Close SPY long
```

More: [examples/telegram](examples/telegram/README.md).

### Python

A script needs `requests` and the strategy's webhook URL, and no broker SDK:

```python
import os
import requests

url = os.environ["NYRIA_WEBHOOK_URL"]
alert = {"ticker": "AAPL", "action": "OPEN", "direction": "LONG"}
response = requests.post(url, json=alert, timeout=10)
print(response.status_code, response.json())
```

More: [examples/python](examples/python/README.md).

### Custom webhooks

Any program that can make an HTTPS `POST` works, with JSON or a line of text:

```sh
curl -X POST "$NYRIA_WEBHOOK_URL" -H "Content-Type: application/json" \
  -d '{ "ticker": "AAPL", "action": "OPEN", "direction": "LONG", "order_type": "market" }'
```

The answer is `200` with `"status": "processed"` when Nyria handed the alert to your bots. That is not a fill. More: [examples/webhook](examples/webhook/README.md).

## Options, single and multi-leg

Options strategies hold up to 4 legs, all on one expiration, which covers single calls and puts, verticals and iron condors. Calendars, diagonals and ratio spreads cannot be built. A spread goes to the broker as one order. The contract comes from one of two places:

- **From my rules.** The alert only says the direction. The strategy's leg rules pick the strike and expiration, by delta, by strikes from at-the-money, by target price or as an offset from another leg. TradingView options strategies always work this way.
- **Provided in alert.** The alert names the contract. Use it with Discord, Telegram or your own code.

A single call named in a webhook:

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

A call spread, as one order:

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
    },
    {
      "side": "CALL",
      "strike": 785,
      "expiration": "2026-12-18",
      "action": "sell_to_open"
    }
  ]
}
```

The same idea in chat:

```text
BTO SPY 12/18 780C
SPY 12/18 780C/785C bull call spread
```

Change the strikes and the expiration to a contract that exists on the day you use them. The checker fails an example whose date has passed. A spread has defined risk only when every leg fills; if a broker rejects a protective long leg, a short leg can be left open. Files: [`option-call-by-legs.json`](examples/webhook/schwab/option-call-by-legs.json), [`option-call-spread.json`](examples/webhook/schwab/option-call-spread.json), [`option-iron-condor.json`](examples/webhook/schwab/option-iron-condor.json).

## Crypto

Crypto spot trades at Alpaca and on Nyria Paper. Schwab and Tradier do not carry it, and tastytrade disabled crypto in its API on 29 June 2026. Use a crypto ticker such as `BTCUSD`:

```json
{
  "ticker": "BTCUSD",
  "action": "OPEN",
  "direction": "LONG"
}
```

Crypto orders go to Alpaca as good till canceled, in fractions: a $100 entry with BTC at $64,000 buys 0.00156 BTC. Folders: [Alpaca](examples/tradingview/alpaca/README.md) and [Nyria Paper](examples/tradingview/nyria-paper/README.md).

## How an alert is read

- An alert needs a ticker, a direction (long or short) and an action (open or close), as JSON or as words. There is no fixed template.
- `ticker`, `instrument` and `symbol` mean the same thing. `action` is `OPEN` or `CLOSE`; Nyria also maps `buy` and `sell`, and reads them against the strategy's settings.
- An alert cannot set the size of an entry. Each bot sizes every order from its own budget per entry, and a `quantity` or `notional` key is ignored.
- Nyria places market and limit orders only. It attaches no stop or target; exits come from your exit alerts.
- A close closes the whole open position. There is no partial-close field.
- An identical body that repeats straight after the first is dropped as a duplicate, so a double send does not open two positions.
- A `200` from the webhook means Nyria read the alert and handed it to your bots. It does not mean the broker filled anything. The bot's Logs tab shows what the broker did.
- TradingView can send an alert up to a minute late, and Discord, Telegram and TrendSpider add their own delivery time. Plan for 30 to 60 seconds.

## Check an alert before it fires

- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert, pick the source and asset type, and read the order Nyria would send, or the refusal word for word. Nothing is traded and no account is needed.
- [TradingView alert message builder](https://nyria.io/tools/tradingview-alert-builder): builds the message for a stock, option or crypto alert.

To check this repository's examples yourself:

```sh
python3 scripts/check_examples.py              # every example, about 15 minutes
python3 scripts/check_examples.py --only tradingview/indicator-long-entry
python3 scripts/check_examples.py --offline    # file and date checks only
```

The script needs only the Python 3 standard library. The tester is rate limited, so the script waits between requests, asks once for each distinct alert, and stops with a message if the tester asks for a long wait, in which case rerun the rest later with --only. The parser reads free text with a language model, so a worded line that passed once can be refused later; the checker retries a temporary "unavailable" answer, and a real change in reading shows up as a FAIL. An option example fails once its expiration date has passed; change the date in the files and in `alerts.json`. TrendSpider bodies are tested as webhook alerts, with the variables filled in.

## Guides

- [Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [TradingView webhook JSON format](https://nyria.io/guides/tradingview-webhook-json-format)
- [TradingView webhook not working: a checklist](https://nyria.io/guides/tradingview-webhook-not-working)
- [Why is my TradingView alert not firing?](https://nyria.io/guides/tradingview-alerts-not-firing)
- [Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Discord alerts to broker orders](https://nyria.io/guides/discord-alerts-to-broker)
- [Telegram alerts to broker orders](https://nyria.io/guides/telegram-alerts-to-broker)
- [Which brokers TradingView alerts can trade](https://nyria.io/guides/which-brokers-tradingview-alerts-can-trade)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- Every source and broker pair, for example [TradingView to Alpaca](https://nyria.io/automate/tradingview-to-alpaca), is listed under [nyria.io/automate](https://nyria.io/automate).

## Repository layout

| Path | Contents |
|---|---|
| [`examples/`](examples/README.md) | One folder for each source and broker pair, such as `examples/tradingview/schwab`, with a README and the alert files |
| [`FAQ.md`](FAQ.md) | Short answers to the questions traders ask most |
| [`alerts.json`](alerts.json) | Every example, the source and asset type it is tested under, and the reading it must produce |
| [`scripts/check_examples.py`](scripts/check_examples.py) | Runs `alerts.json` through the alert tester |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to add or fix an example |

How alert-to-order automation works, step by step: [Nyria-LLC/trading-alert-automation](https://github.com/Nyria-LLC/trading-alert-automation).

Found an example the tester rejects or reads differently? Open an issue and name the example id.

## Not financial advice

Nothing here is financial advice or a trading strategy, and these examples say nothing about how any strategy performs. An automated order can lose money. You are responsible for the alerts you send, the orders they place and the account they trade in. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and test on paper first.

## License

[MIT](LICENSE)
