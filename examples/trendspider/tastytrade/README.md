# TrendSpider alerts to tastytrade

To automate TrendSpider alerts to tastytrade, create a Nyria strategy with TrendSpider as the alert source, connect your tastytrade account, and set the strategy's webhook URL in TrendSpider. The alert body carries the symbol and a `buy` or `sell` action. Nyria places the order in your tastytrade account. Your TrendSpider plan has to include webhook alerts.

## What you need

- A TrendSpider plan that includes webhook alerts.
- A free Nyria account and your tastytrade account. Test on paper first; live trading is from $15 a month.

## How do I set up TrendSpider alerts to tastytrade?

1. Connect tastytrade. In Nyria, select Integrations, then the tastytrade card. Under Live trading select Connect live account. Sign in at tastytrade and select Authorize. Nyria imports every account under the login, and you pick the one a bot trades.
2. Create a strategy. Select Create strategy and pick TrendSpider as the alert source. Choose stocks or options as the asset type, and set what an entry and an exit do on each side.
3. Set the webhook in TrendSpider. For Alerts, open User Icon, then Account & Settings, check Webhook, paste the URL from the strategy's Integration tab (`https://trades.nyria.io/webhooks/<your-strategy-token>`) and use method POST. That URL covers every alert on the account, so Alerts can feed one Nyria strategy.
4. To feed several strategies, use Strategy Bots instead. Each bot has its own webhook URL and body, so each can post to a different Nyria strategy.
5. Paste a body from the list below into the alert's note. TrendSpider posts the note as the request body, and sends it as application/json when it is valid JSON. Select Send Test Alert, then set the TrendSpider alert Active.
6. Back in Nyria, select Check format on the strategy, then Check and save. The strategy turns Active once Nyria reads every side, and the Logs tab shows the ticker, side and contract it read.
7. Deploy a bot. Select Deploy bot, pick the tastytrade account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. tastytrade connects live accounts only. Run the strategy on Nyria Paper first, then deploy a second bot on the tastytrade account.

## What must the alert say?

Nyria needs three things from an alert: a ticker, a direction (long or short) and an action (open or close). There is no fixed template. TrendSpider has no action variable, so write `buy` into each entry alert and `sell` into each exit alert. Leave quantity out; the bot sizes the order. Variables are written `%alert_symbol%` for Alerts and `%bot_symbol%` for Strategy Bots, not `{{...}}`.

## Alert messages

Each message below is a file in this folder and is read back by Nyria's alert tester through [`scripts/check_examples.py`](../../../scripts/check_examples.py). The ticker and sample values are placeholders; use your own.

### Alerts: one account-wide webhook URL

**Alert, entry.** Buys. On a long-only strategy that opens a long; on a strategy that trades both sides it covers an open short, and otherwise opens a long.

```json
{
  "symbol": "%alert_symbol%",
  "action": "buy",
  "price": "%last_price%"
}
```

File: [`alert-buy.json`](alert-buy.json)

**Alert, exit.** Sells. On a long-only strategy that closes the long.

```json
{
  "symbol": "%alert_symbol%",
  "action": "sell",
  "price": "%last_price%"
}
```

File: [`alert-sell.json`](alert-sell.json)

### Strategy Bots: one URL for each bot

**Strategy Bot, entry webhook.** The same body with %bot_symbol%, set on the bot's entry webhook.

```json
{
  "symbol": "%bot_symbol%",
  "action": "buy",
  "price": "%last_price%"
}
```

File: [`strategy-bot-buy.json`](strategy-bot-buy.json)

**Strategy Bot, exit webhook.** The same body with %bot_symbol%, set on the bot's exit webhook.

```json
{
  "symbol": "%bot_symbol%",
  "action": "sell",
  "price": "%last_price%"
}
```

File: [`strategy-bot-sell.json`](strategy-bot-sell.json)

## How do options alerts work at tastytrade?

tastytrade takes options as single legs or spreads of up to 4 legs, sent as one order. With contract selection set to From my rules, send the same directional alert as for a stock and Nyria picks the contract from the strategy's strike, delta and days-to-expiry settings. Strikes and spreads written into an alert are covered by the custom webhook examples, and the webhook reference lists every field.

## Can I trade crypto at tastytrade?

No. Crypto trading has been disabled through tastytrade's API since 29 June 2026. A crypto alert fails the entry with a crypto unavailable notice. Use Alpaca or Nyria Paper for crypto. See the [Alpaca folder](../alpaca/README.md) and the [Nyria Paper folder](../nyria-paper/README.md) for crypto spot.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Trade crypto at tastytrade.** tastytrade does not carry crypto through Nyria. Use Alpaca or Nyria Paper.

## tastytrade notes

- Live accounts only, connected through tastytrade's own sign-in. The password goes to tastytrade and never to Nyria.
- Market and limit orders. A spread goes as one order for all its legs, priced as a net debit or credit when it is a limit order.
- Day and Good till canceled go to tastytrade as set. tastytrade has no fill or kill, so a strategy set to Fill or kill sends Day.
- Stocks in whole shares and options in whole contracts. Defined-risk spreads need options level 3 or higher at tastytrade.
- Crypto trading has been disabled through tastytrade's API since 29 June 2026. A crypto alert fails the entry with a crypto unavailable notice. Use Alpaca or Nyria Paper for crypto.
- MODIFY is refused at tastytrade. To re-price a resting entry, send CANCEL, then a new OPEN.

## Links

- [How to automate TrendSpider alerts to tastytrade](https://nyria.io/automate/trendspider-to-tastytrade): the step-by-step page on nyria.io
- [TrendSpider on Nyria](https://nyria.io/signals/trendspider)
- [Guide: Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [tastytrade on Nyria](https://nyria.io/integrations/tastytrade) and [the tastytrade docs](https://docs.nyria.io/integrations/brokers/tastytrade)
- [TrendSpider setup in the docs](https://docs.nyria.io/alerts/trendspider)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
