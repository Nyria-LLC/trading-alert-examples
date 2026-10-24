# TrendSpider alerts to a broker

TrendSpider posts an alert's note to your Nyria strategy's webhook URL as the request body, Nyria reads it, and each bot on the strategy places the order in its own account: Charles Schwab, Tradier, tastytrade, Alpaca or Nyria Paper, the free simulated broker.

You need a TrendSpider plan that includes webhook alerts. TrendSpider's pricing page lists which tiers do.

## Pick your broker

| Broker | Alert bodies and setup |
|---|---|
| Charles Schwab | [TrendSpider alerts to Charles Schwab](schwab/README.md) |
| Tradier | [TrendSpider alerts to Tradier](tradier/README.md) |
| tastytrade | [TrendSpider alerts to tastytrade](tastytrade/README.md) |
| Alpaca | [TrendSpider alerts to Alpaca](alpaca/README.md), with crypto |
| Nyria Paper | [TrendSpider alerts to Nyria Paper](nyria-paper/README.md), with crypto |

The body does not change with the broker. The bot you deploy decides where the order goes.

## Alerts or Strategy Bots?

TrendSpider sends webhooks from two places, and they behave differently.

| | Alerts (price, indicator, scanner) | Strategy Bots |
|---|---|---|
| Webhook URL | One URL for the whole account (Account & Settings) | A URL and body for each bot |
| Symbol variable | `%alert_symbol%` | `%bot_symbol%` |
| Can feed several Nyria strategies | No. Every alert goes to the one account URL | Yes. Each bot can post to a different strategy |

To run several Nyria strategies from one TrendSpider account, use Strategy Bots.

## What does the body need?

TrendSpider has no action or quantity variable. Write `"action": "buy"` into each entry alert and `"action": "sell"` into each exit alert, and leave quantity out so the Nyria bot sizes the order. TrendSpider fills `%alert_symbol%`, `%bot_symbol%` and `%last_price%` when the alert fires. On a long-only strategy `buy` opens a long and `sell` closes it. On a strategy that trades both sides, `buy` covers an open short and otherwise opens a long, and `sell` closes an open long and otherwise opens a short.

To place a limit order, set the strategy's order type to limit and its limit target to Alert price, so `%last_price%` becomes the limit price. The docs describe when Nyria reads `order_type` from the body.

For options with contract selection set to "From my rules", send the same directional body and Nyria picks the contract from the strategy's strike, delta and days-to-expiry settings. For strikes, multi-leg spreads and dollar-notional crypto, see the [webhook examples](../webhook/README.md) and the [webhook reference](https://docs.nyria.io/webhook-reference).

## Links

- [TrendSpider setup in the docs](https://docs.nyria.io/alerts/trendspider)
- [TrendSpider alerts on Nyria](https://nyria.io/signals/trendspider)
- [Alert tester](https://nyria.io/tools/alert-tester): TrendSpider bodies are read as webhook alerts. Paste one with the variables filled in.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
