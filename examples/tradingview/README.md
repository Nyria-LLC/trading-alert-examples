# TradingView alerts to a broker

TradingView posts an alert's message to your Nyria strategy's webhook URL, Nyria reads it, and each bot on the strategy places the order in its own account: Charles Schwab, Tradier, tastytrade, Alpaca or Nyria Paper, the free simulated broker.

You need a paid TradingView plan with two-factor sign-in on, because the free plan cannot send webhooks. The webhook URL is on the Integration tab of your Nyria strategy and looks like `https://trades.nyria.io/webhooks/<your-strategy-token>`. The token is the only authentication, so do not commit it.

## Pick your broker

| Broker | Alert messages and setup |
|---|---|
| Charles Schwab | [TradingView alerts to Charles Schwab](schwab/README.md) |
| Tradier | [TradingView alerts to Tradier](tradier/README.md) |
| tastytrade | [TradingView alerts to tastytrade](tastytrade/README.md) |
| Alpaca | [TradingView alerts to Alpaca](alpaca/README.md), with crypto |
| Nyria Paper | [TradingView alerts to Nyria Paper](nyria-paper/README.md), with crypto |

The alert does not change with the broker. The same message works for all five, and the bot you deploy decides where the order goes. Each folder lists the messages that apply to that broker and the broker's own limits. Every message is read back by Nyria's alert tester through [`../../scripts/check_examples.py`](../../scripts/check_examples.py), with the placeholders filled in the way TradingView fills them before it sends.

## How do I create the alert?

1. Press Alt+A (Option+A on a Mac) on the chart.
2. Condition: your strategy, with "Order fills only", or your indicator with Trigger set to Once Per Bar Close.
3. Expiration: open-ended if your plan offers it. An expired alert stops firing without warning.
4. Message: paste one of the messages from a broker folder.
5. Notifications: tick "Webhook URL" and paste the URL from the Integration tab.
6. Create. In Nyria, select Check format on the strategy, then run it on a paper bot first.

An alert cannot set the size of an entry. Each bot sizes every order from its own budget per entry, so none of these messages carries a quantity.

## Strategy or indicator?

A `strategy()` script has the `{{strategy.*}}` placeholders. One alert set to "Order fills only" fires on every fill, and the placeholders say which side filled. Nyria works out the action and direction from the change in position: `buy` with `long` after `flat` opens a long, `sell` with `flat` after `long` closes it, and `sell` with `short` after `flat` opens a short. See `strategy-order-fills.json` in any broker folder.

An `indicator()` has no `{{strategy.*}}` values. An alert that carries them sends the placeholder text as typed and nothing trades. Write the side into the message and create one alert per side, as in `indicator-long-entry.json` and `indicator-long-exit.json`. `{{ticker}}` and `{{close}}` work on both kinds of script. A close closes the whole open position; there is no partial-close field.

An indicator traded on four sides across five tickers means twenty alerts. As a strategy, the same script needs five. The [docs](https://docs.nyria.io/alerts/tradingview/indicator-to-strategy) walk through the conversion.

## Which TradingView placeholders work?

| Placeholder | Becomes |
|---|---|
| `{{ticker}}` | The chart symbol, for example `SPY` |
| `{{close}}` | Confirmed bar close |
| `{{strategy.order.action}}` | `buy` or `sell` |
| `{{strategy.market_position}}` | `long`, `short` or `flat` after the fill |
| `{{strategy.prev_market_position}}` | The position before the fill |
| `{{strategy.order.contracts}}` | Order size, for reference only |
| `{{timenow}}` | Alert fire time, UTC |

TradingView fills only the placeholders it publishes. A name it does not know, such as `{{syminfo.ticker}}`, arrives as typed. Inside a Pine `alert()` string, join the value in instead: `'{"instrument":"' + syminfo.ticker + '"}'`.

## Options and crypto

TradingView options strategies always use "From my rules": the alert says the direction and the strategy's leg rules pick the strike and expiration. `options-by-rules-entry.json` is the same message as a stock, and `options-spread-limit-entry.json` adds a net limit price for a multi-leg entry. Options go to Schwab, Tradier, tastytrade and Alpaca as single legs or spreads of up to 4 legs.

Crypto spot works at Alpaca and on Nyria Paper with the same message shape on a crypto ticker such as `BTCUSD`. Schwab, Tradier and tastytrade do not carry crypto through Nyria.

## Pine Script v6

| File | What it shows |
|---|---|
| [`pine/indicator_alert.pine`](pine/indicator_alert.pine) | An indicator that calls `alert()` with a JSON message. One alert on the indicator covers every call. |
| [`pine/strategy_alert_message.pine`](pine/strategy_alert_message.pine) | A strategy that sets `alert_message` on `strategy.entry()` and `strategy.close()`. The alert's Message box holds `{{strategy.order.alert_message}}`. |

Both build the message from `syminfo.ticker` in Pine, so they need no placeholders. The SMA cross in both files is a plumbing example for the alert message, not a trading idea. A repainting indicator fires differently live than it plots on past bars, so check yours before it trades. For a longer, configurable script, see the Nyria Alert Builder in [trading-alert-automation](https://github.com/Nyria-LLC/trading-alert-automation/tree/main/examples/tradingview).

## Links

- [TradingView alert message builder](https://nyria.io/tools/tradingview-alert-builder): fills in a message for a stock, option or crypto alert.
- [Alert tester](https://nyria.io/tools/alert-tester): paste a message and read the order Nyria would send. Nothing is traded and no account is needed.
- [Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [TradingView webhook JSON format](https://nyria.io/guides/tradingview-webhook-json-format)
- [TradingView webhook not working: a checklist](https://nyria.io/guides/tradingview-webhook-not-working)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
