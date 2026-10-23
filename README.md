# trading-alert-examples

Copy-pasteable trading alerts that [Nyria](https://nyria.io) reads and turns into orders in your own brokerage account: TradingView alert messages (JSON and plain text), Pine Script v6 that sends them, webhook senders in curl, Python and Node, and the message lines a caller can post in Discord or Telegram.

Nyria places the order at Charles Schwab, Tradier, tastytrade or Alpaca, or on Nyria Paper, a free simulated broker. Every alert in this repository is listed in [`alerts.json`](alerts.json) and run through Nyria's public [alert tester](https://nyria.io/tools/alert-tester) by [`scripts/check_examples.py`](scripts/check_examples.py), so each one is read the way the table below says it is.

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

Using an indicator instead of a strategy, or a stock, option or crypto alert, or no TradingView at all? See the table.

## Formats

| What | Example | Source | More |
|---|---|---|---|
| Strategy, side from TradingView's placeholders | the JSON above | TradingView strategy | [tradingview](tradingview/README.md#strategy-alerts-one-alert-for-every-fill) |
| Strategy, plain text | `{{strategy.order.action}} {{ticker}} @ {{close}}` | TradingView strategy | [tradingview](tradingview/README.md#strategy-alerts-one-alert-for-every-fill) |
| Indicator, long entry | `{ "action": "OPEN", "instrument": "{{ticker}}", "direction": "LONG" }` | TradingView indicator, webhook | [tradingview](tradingview/README.md#indicator-alerts-one-alert-per-side) |
| Indicator, exit | `{ "action": "CLOSE", "instrument": "{{ticker}}", "direction": "LONG" }` | TradingView indicator, webhook | [tradingview](tradingview/README.md#indicator-alerts-one-alert-per-side) |
| Options, contract picked by the strategy's rules (delta, strikes from at-the-money) | the same JSON as a stock | TradingView, webhook | [tradingview](tradingview/README.md#options) |
| Options, contract named in the alert | `legs` array with `side`, `strike`, `expiration`, `action` | webhook, TradingView | [payload](webhook/payloads/option-call-by-legs.json), [spread](webhook/payloads/option-call-spread.json) |
| Options, one line of notation | `BTO SPY 12/18 780C` | Discord, Telegram | [discord-telegram](discord-telegram/README.md#options) |
| Crypto | `{ "action": "OPEN", "instrument": "{{ticker}}", "direction": "LONG" }` on a crypto ticker such as BTCUSD | TradingView, webhook | [tradingview](tradingview/README.md#crypto) |
| Closing and exits | `{ "ticker": "AAPL", "action": "CLOSE", "direction": "LONG" }` or `Close SPY long` | every source | [webhook](webhook/README.md#payloads) |
| Plain-text sentence | `SPY long entry`, `long SPY here` | every source | [discord-telegram](discord-telegram/README.md#stocks-and-etfs) |
| Limit order | `order_type` `limit` with a `price` | webhook, TradingView | [payload](webhook/payloads/stock-open-limit.json) |

Pine Script that builds and sends these messages: [`tradingview/indicator_alert.pine`](tradingview/indicator_alert.pine) (an `alert()` call) and [`tradingview/strategy_alert_message.pine`](tradingview/strategy_alert_message.pine) (`alert_message` on each order).

## How an alert is read

- An alert needs a ticker, a direction (long or short) and an action (open or close), as JSON or as words. There is no fixed template.
- `ticker`, `instrument` and `symbol` mean the same thing. `action` is `OPEN` or `CLOSE`; Nyria also maps `buy` and `sell`, and reads them against the strategy's settings.
- An alert cannot set the size of an entry. Each bot sizes every order from its own budget per entry, and a `quantity` or `notional` key is ignored.
- Nyria places market and limit orders only. It attaches no stop or target; exits come from your exit alerts.
- An identical body that repeats straight after the first is dropped as a duplicate, so a double send does not open two positions.
- A `200` from the webhook means Nyria read the alert and handed it to your bots. It does not mean the broker filled anything. The bot's Logs tab shows what the broker did.

## Check an alert before it fires

- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert, pick the source and asset type, and read the order Nyria would send, or the refusal word for word. Nothing is traded and no account is needed.
- [TradingView alert message builder](https://nyria.io/tools/tradingview-alert-builder): builds the message for a stock, option or crypto alert.

To check this repository's examples yourself:

```sh
python3 scripts/check_examples.py              # every example, about 5 minutes
python3 scripts/check_examples.py --only tv-indicator-long-entry
python3 scripts/check_examples.py --offline    # file and date checks only
```

The script needs only the Python 3 standard library. The tester is rate limited, so the script waits between requests and stops with a message if the tester asks for a long wait. The parser reads free text with a language model, so a worded line that passed once can be refused later; the checker retries a temporary "unavailable" answer, and a real change in reading shows up as a FAIL. An option example fails once its expiration date has passed; change the date in `alerts.json` and in the file that shows it.

## Guides

- [Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [TradingView webhook not working: a checklist](https://nyria.io/guides/tradingview-webhook-not-working)
- [Send alerts from your Python script to your broker](https://nyria.io/guides/python-webhook-alerts-to-broker)
- [Discord alerts to broker orders](https://nyria.io/guides/discord-alerts-to-broker)
- [Telegram alerts to broker orders](https://nyria.io/guides/telegram-alerts-to-broker)
- [Which brokers TradingView alerts can trade](https://nyria.io/guides/which-brokers-tradingview-alerts-can-trade)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- Source by broker pairs, for example [TradingView to Alpaca](https://nyria.io/automate/tradingview-to-alpaca), are under [nyria.io/automate](https://nyria.io/automate).

## Brokers

| Broker | Stocks and ETFs | Options | Crypto spot | Paper |
|---|---|---|---|---|
| Charles Schwab | yes | yes, up to 4 legs | no | no, use Nyria Paper |
| Tradier | yes | yes, up to 4 legs | no | Tradier Sandbox |
| tastytrade | yes | yes, up to 4 legs | no | no, use Nyria Paper |
| Alpaca | yes | yes, up to 4 legs | yes | Alpaca paper account |
| Nyria Paper | yes | yes | yes | free simulated broker |

Paper is free. Live trading from $15 a month; see [nyria.io/pricing](https://nyria.io/pricing). TradingView webhooks need a paid TradingView plan.

## Repository layout

| Path | Contents |
|---|---|
| [`tradingview/`](tradingview) | Alert messages and two Pine Script v6 examples |
| [`webhook/`](webhook) | curl, Python and Node senders, and payloads |
| [`discord-telegram/`](discord-telegram) | Message lines Nyria reads in a Discord channel or Telegram chat |
| [`alerts.json`](alerts.json) | Every example, the source and asset type it is tested under, and the reading it must produce |
| [`scripts/check_examples.py`](scripts/check_examples.py) | Runs `alerts.json` through the alert tester |

Found an example the tester rejects or reads differently? Open an issue and name the example id.

## Not financial advice

Nothing here is financial advice or a trading strategy, and these examples say nothing about how any strategy performs. An automated order can lose money. You are responsible for the alerts you send, the orders they place and the account they trade in. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and test on paper first.

## License

[MIT](LICENSE)
