# TradingView

Alert messages and Pine Script v6 that Nyria reads. TradingView posts the message to your strategy's webhook URL, Nyria reads it, and each bot on the strategy places the order in its own account.

You need a paid TradingView plan with two-factor sign-in on, because the free plan cannot send webhooks. The webhook URL is on the Integration tab of your Nyria strategy and looks like `https://trades.nyria.io/webhooks/<your-strategy-token>`. The token is the only authentication, so do not commit it.

Every message below is listed in [`../alerts.json`](../alerts.json) and read back by Nyria's alert tester through [`../scripts/check_examples.py`](../scripts/check_examples.py). The placeholders are filled with sample values first, the way TradingView fills them before it sends.

## Set up the alert

1. Press Alt+A (Option+A on a Mac) on the chart.
2. Condition: your strategy, with "Order fills only", or your indicator.
3. Message: paste one of the messages below.
4. Notifications: tick "Webhook URL" and paste the URL from the Integration tab.
5. Create. In Nyria, select Check format on the strategy, then run it on a paper bot first.

An alert cannot set the size of an entry. Each bot sizes every order from its own budget per entry, so none of these messages carries a quantity.

## Strategy alerts: one alert for every fill

A `strategy()` script has the `{{strategy.*}}` placeholders. One alert set to "Order fills only" fires on every fill, and the placeholders say which side filled.

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

File: [`messages/strategy-default.json`](messages/strategy-default.json). Nyria works out the action and direction from the change in position: `buy` with `long` after `flat` opens a long, `sell` with `flat` after `long` closes it, and `sell` with `short` after `flat` opens a short. `price` is an unquoted number in the message, so the text is valid JSON only after TradingView fills `{{close}}`.

The same thing as a plain sentence:

```text
{{strategy.order.action}} {{ticker}} @ {{close}}
```

File: [`messages/strategy-plain.txt`](messages/strategy-plain.txt). TradingView's own default strategy message also reads, so an alert you already have can stay as it is:

```text
order {{strategy.order.action}} @ {{strategy.order.contracts}} filled on {{ticker}}. New strategy position is {{strategy.position_size}}
```

File: [`messages/tradingview-default-strategy.txt`](messages/tradingview-default-strategy.txt).

## Indicator alerts: one alert per side

An `indicator()` has no `{{strategy.*}}` values. An alert that carries them sends the placeholder text as typed and nothing trades. Write the side into the message and create one alert per side. `{{ticker}}` and `{{close}}` work on both kinds of script.

Long entry:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

Long exit:

```json
{
  "action": "CLOSE",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

Short entry and short exit use the same shape with `"direction": "SHORT"`. Files: [`indicator-long-entry.json`](messages/indicator-long-entry.json), [`indicator-long-exit.json`](messages/indicator-long-exit.json), [`indicator-short-entry.json`](messages/indicator-short-entry.json), [`indicator-short-exit.json`](messages/indicator-short-exit.json). A close closes the whole open position; there is no partial-close field.

A resting limit order takes `order_type` and `price`:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG",
  "order_type": "limit",
  "price": {{close}}
}
```

File: [`messages/indicator-limit-entry.json`](messages/indicator-limit-entry.json). Nyria reads `order_type` on alerts that name both `action` and `direction`, as these do. On a TradingView position-change message (the strategy message above) it uses the order type set on the strategy.

## Options

For options, the message decides how the contract is chosen, and the strategy setting has to match.

**From my rules.** The alert only says the direction. The strategy's leg rules pick the strike and expiration, by delta, by strikes from at-the-money or as an offset from another leg. The webhook has no field for delta or days to expiry. The message is the same as for a stock:

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

Files: [`options-by-rules-entry.json`](messages/options-by-rules-entry.json) and [`options-by-rules-exit.json`](messages/options-by-rules-exit.json).

**Provided in alert.** The alert carries a `legs` array with one entry per leg. Give `expiration` as `YYYY-MM-DD` on every entry leg, and use an expiration that is a real trading day. Change the strike and date to a contract that exists when you use it.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
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

File: [`messages/options-legs-entry.json`](messages/options-legs-entry.json). A spread is more entries in `legs`; see [`../webhook/payloads/option-call-spread.json`](../webhook/payloads/option-call-spread.json).

## Crypto

The same shape works with a crypto ticker. Set `{{ticker}}` from a crypto chart (it gives `BTCUSD`, for example) and use a strategy whose asset type is crypto.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

Files: [`messages/crypto-entry.json`](messages/crypto-entry.json) and [`messages/crypto-exit.json`](messages/crypto-exit.json).

## Pine Script v6

| File | What it shows |
|---|---|
| [`indicator_alert.pine`](indicator_alert.pine) | An indicator that calls `alert()` with a JSON message. One alert on the indicator covers every call. |
| [`strategy_alert_message.pine`](strategy_alert_message.pine) | A strategy that sets `alert_message` on `strategy.entry()` and `strategy.close()`. The alert's Message box holds `{{strategy.order.alert_message}}`. |

Both build the message from `syminfo.ticker` in Pine, so they need no placeholders. TradingView fills only its own placeholders: a name it does not know, such as `{{syminfo.ticker}}`, arrives as typed.

The SMA cross in both files is a plumbing example for the alert message, not a trading idea. A repainting indicator fires differently live than it plots on past bars, so check yours before it trades.

## Links

- [TradingView alert message builder](https://nyria.io/tools/tradingview-alert-builder): fills in a message for a stock, option or crypto alert.
- [Alert tester](https://nyria.io/tools/alert-tester): paste a message and read the order Nyria would send. Nothing is traded and no account is needed.
- [Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [TradingView webhook not working: a checklist](https://nyria.io/guides/tradingview-webhook-not-working)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
