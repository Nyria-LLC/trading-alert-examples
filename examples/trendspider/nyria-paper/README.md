# TrendSpider alerts to Nyria Paper

To automate TrendSpider alerts to Nyria Paper, create a Nyria strategy with TrendSpider as the alert source, deploy a bot on Nyria Paper, the free simulated broker, and set the strategy's webhook URL in TrendSpider. The alert body carries the symbol and a `buy` or `sell` action. Nyria fills it as a simulated order, so no real money moves. Your TrendSpider plan has to include webhook alerts.

## What you need

- A TrendSpider plan that includes webhook alerts.
- A free Nyria account. Nyria Paper needs no broker and no card.

## How do I set up TrendSpider alerts to Nyria Paper?

1. Create the account. In Nyria, select Integrations, then the Nyria Paper card, then Create Nyria Paper account. It opens with a simulated balance and needs no broker, API key or card.
2. Create a strategy. Select Create strategy and pick TrendSpider as the alert source. Choose stocks, options or crypto as the asset type, and set what an entry and an exit do on each side.
3. Set the webhook in TrendSpider. For Alerts, open User Icon, then Account & Settings, check Webhook, paste the URL from the strategy's Integration tab (`https://trades.nyria.io/webhooks/<your-strategy-token>`) and use method POST. That URL covers every alert on the account, so Alerts can feed one Nyria strategy.
4. To feed several strategies, use Strategy Bots instead. Each bot has its own webhook URL and body, so each can post to a different Nyria strategy.
5. Paste a body from the list below into the alert's note. TrendSpider posts the note as the request body, and sends it as application/json when it is valid JSON. Select Send Test Alert, then set the TrendSpider alert Active.
6. Back in Nyria, select Check format on the strategy, then Check and save. The strategy turns Active once Nyria reads every side, and the Logs tab shows the ticker, side and contract it read.
7. Deploy a bot. Select Deploy bot, choose Nyria Paper on the Account step and set a Budget per entry. The next alert becomes a simulated order.

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

## How do options alerts work at Nyria Paper?

Nyria Paper takes options as single legs or spreads of up to 4 legs, sent as one order. With contract selection set to From my rules, send the same directional alert as for a stock and Nyria picks the contract from the strategy's strike, delta and days-to-expiry settings. Strikes and spreads written into an alert are covered by the custom webhook examples, and the webhook reference lists every field.

## Can I trade crypto at Nyria Paper?

Nyria Paper fills crypto spot at any hour, weekends included, from the live quote. Use a strategy whose asset type is crypto. A short form such as `BTC` or `BTCUSD` works while only one selected pair matches it; if you select both the USDT and the USDC pair for a coin, the alert must name the full pair.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.

## Nyria Paper notes

- Simulated end to end: no order reaches a broker or exchange and no money moves.
- Stocks, options (single legs and spreads up to 4 legs) and crypto spot.
- A market order fills at the ask to buy and the bid to sell, from the quote Nyria read when the alert arrived. A limit order fills or is refused at once against that quote.
- Options alerts are refused while the options market is closed, and the log says so. Stocks and crypto fill at any hour.
- There is no slippage, so paper results usually read better than a live account would on the same alerts.
- Nothing queues, so there is no working order to MODIFY or CANCEL.

## Links

- [How to automate TrendSpider alerts to Nyria Paper](https://nyria.io/automate/trendspider-to-paper): the step-by-step page on nyria.io
- [TrendSpider on Nyria](https://nyria.io/signals/trendspider)
- [Guide: Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts)
- [Nyria Paper on Nyria](https://docs.nyria.io/integrations/brokers/nyria-paper) and [the Nyria Paper docs](https://docs.nyria.io/integrations/brokers/nyria-paper)
- [TrendSpider setup in the docs](https://docs.nyria.io/alerts/trendspider)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [Paper trade a TradingView strategy for free](https://nyria.io/guides/paper-trade-tradingview-strategy-free)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
