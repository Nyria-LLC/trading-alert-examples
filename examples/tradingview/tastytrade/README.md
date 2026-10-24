# TradingView alerts to tastytrade

To automate TradingView alerts to tastytrade, create a Nyria strategy with TradingView as the alert source, connect your tastytrade account, and paste the strategy's webhook URL into the alert's Webhook URL box. The alert message names a ticker, a side and whether it opens or closes a position. Nyria places the order in your tastytrade account. TradingView sends webhooks on paid plans only, with two-factor sign-in turned on.

## What you need

- A TradingView plan that sends webhooks (paid, with two-factor sign-in on). The free plan cannot.
- A free Nyria account and your tastytrade account. Test on paper first; live trading is from $15 a month.

## How do I set up TradingView alerts to tastytrade?

1. Connect tastytrade. In Nyria, select Integrations, then the tastytrade card. Under Live trading select Connect live account. Sign in at tastytrade and select Authorize. Nyria imports every account under the login, and you pick the one a bot trades.
2. Create a strategy. Select Create strategy and pick TradingView as the alert source. Choose stocks or options as the asset type, and set what an entry and an exit do on each side.
3. Create the alert in TradingView. Press Alt+A (Option+A on a Mac) on the chart. Set Condition to your strategy and choose Order fills only, or to your indicator with Trigger set to Once Per Bar Close.
4. Set Expiration to open-ended if your plan offers it. An expired alert stops firing without warning.
5. Paste a message from the list below into Message. In Notifications tick Webhook URL and paste the strategy's URL from its Integration tab. It looks like `https://trades.nyria.io/webhooks/<your-strategy-token>`. Select Create.
6. Back in Nyria, select Check format on the strategy, then Check and save. The strategy turns Active once Nyria reads every side, and the Logs tab shows the ticker, side and contract it read.
7. Deploy a bot. Select Deploy bot, pick the tastytrade account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. tastytrade connects live accounts only. Run the strategy on Nyria Paper first, then deploy a second bot on the tastytrade account.

## What must the alert say?

Nyria needs three things from an alert: a ticker, a direction (long or short) and an action (open or close). There is no fixed template. JSON, plain text and TradingView's own default strategy message all work. A `strategy()` script has the `{{strategy.*}}` placeholders and needs one Order-fills alert per ticker. An `indicator()` has none, so it needs one alert per side with the side written into the message. A placeholder TradingView does not know, such as `{{syminfo.ticker}}`, arrives as typed and nothing trades.

## Alert messages

Each message below is a file in this folder and is read back by Nyria's alert tester through [`scripts/check_examples.py`](../../../scripts/check_examples.py). The ticker and sample values are placeholders; use your own.

### Strategy alerts: one alert for every fill

**Strategy, any fill.** Reads the side from TradingView's position placeholders: a buy from flat opens a long, a sell back to flat closes it, a sell from flat opens a short. Set the alert to Order fills only.

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

File: [`strategy-order-fills.json`](strategy-order-fills.json)

**Strategy, plain text.** The same idea as a sentence. A buy opens a long on a long-only strategy.

```text
{{strategy.order.action}} {{ticker}} @ {{close}}
```

File: [`strategy-plain-text.txt`](strategy-plain-text.txt)

**TradingView's own default strategy message.** An alert you already have keeps working: Nyria reads the order and the new position size.

```text
order {{strategy.order.action}} @ {{strategy.order.contracts}} filled on {{ticker}}. New strategy position is {{strategy.position_size}}
```

File: [`strategy-default-message.txt`](strategy-default-message.txt)

### Indicator alerts: one alert per side

**Indicator, long entry.** Opens a long. An indicator has no strategy placeholders, so the message says the side.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

File: [`indicator-long-entry.json`](indicator-long-entry.json)

**Indicator, long exit.** Closes the whole open long position.

```json
{
  "action": "CLOSE",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

File: [`indicator-long-exit.json`](indicator-long-exit.json)

**Indicator, short entry.** Opens a short. Short stock needs a margin account.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "SHORT"
}
```

File: [`indicator-short-entry.json`](indicator-short-entry.json)

**Indicator, short exit.** Closes the whole open short position.

```json
{
  "action": "CLOSE",
  "instrument": "{{ticker}}",
  "direction": "SHORT"
}
```

File: [`indicator-short-exit.json`](indicator-short-exit.json)

### Limit orders

**Limit entry at the alert's price.** Opens a long as a limit order at the bar close.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG",
  "order_type": "limit",
  "price": {{close}}
}
```

File: [`limit-entry.json`](limit-entry.json)

### Options

**Option entry, contract from the strategy's rules.** The alert says only the direction. The strategy's leg rules pick the strike and expiration.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

File: [`options-by-rules-entry.json`](options-by-rules-entry.json)

**Option exit.** Closes the option position the bot opened.

```json
{
  "action": "CLOSE",
  "instrument": "{{ticker}}",
  "direction": "LONG"
}
```

File: [`options-by-rules-exit.json`](options-by-rules-exit.json)

**Multi-leg entry at a net price.** Opens the strategy's legs as one spread order, with the alert's price as the net limit.

```json
{
  "action": "OPEN",
  "instrument": "{{ticker}}",
  "direction": "LONG",
  "order_type": "limit",
  "price": 1.50
}
```

File: [`options-spread-limit-entry.json`](options-spread-limit-entry.json)

## How do options alerts work at tastytrade?

tastytrade takes options as single legs or spreads of up to 4 legs, sent as one order. For TradingView the contract always comes from the strategy's leg rules: the alert says the direction, and Nyria picks the strike and expiration by delta, by strikes from at-the-money, by target price or as an offset from another leg. The webhook has no field for delta or days to expiry. To open a spread at a net price, send `order_type` `limit` with a `price`; Nyria builds every leg from the rules and prices the spread at that price.

## Can I trade crypto at tastytrade?

No. Crypto trading has been disabled through tastytrade's API since 29 June 2026. A crypto alert fails the entry with a crypto unavailable notice. Use Alpaca or Nyria Paper for crypto. See the [Alpaca folder](../alpaca/README.md) and the [Nyria Paper folder](../nyria-paper/README.md) for crypto spot.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Outrun delivery delays.** TradingView can send an alert up to a minute late and does not guarantee webhook delivery.
- **Trade crypto at tastytrade.** tastytrade does not carry crypto through Nyria. Use Alpaca or Nyria Paper.

## tastytrade notes

- Live accounts only, connected through tastytrade's own sign-in. The password goes to tastytrade and never to Nyria.
- Market and limit orders. A spread goes as one order for all its legs, priced as a net debit or credit when it is a limit order.
- Day and Good till canceled go to tastytrade as set. tastytrade has no fill or kill, so a strategy set to Fill or kill sends Day.
- Stocks in whole shares and options in whole contracts. Defined-risk spreads need options level 3 or higher at tastytrade.
- Crypto trading has been disabled through tastytrade's API since 29 June 2026. A crypto alert fails the entry with a crypto unavailable notice. Use Alpaca or Nyria Paper for crypto.
- MODIFY is refused at tastytrade. To re-price a resting entry, send CANCEL, then a new OPEN.

## Links

- [How to automate TradingView alerts to tastytrade](https://nyria.io/automate/tradingview-to-tastytrade): the step-by-step page on nyria.io
- [TradingView on Nyria](https://nyria.io/signals/tradingview)
- [Guide: Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [tastytrade on Nyria](https://nyria.io/integrations/tastytrade) and [the tastytrade docs](https://docs.nyria.io/integrations/brokers/tastytrade)
- [TradingView setup in the docs](https://docs.nyria.io/alerts/tradingview)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [TradingView alert message builder](https://nyria.io/tools/tradingview-alert-builder)
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
