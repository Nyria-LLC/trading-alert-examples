# Telegram alerts to Nyria Paper

To automate Telegram alerts to Nyria Paper, add Nyria to a Telegram group or channel you run, point a Nyria strategy at it, and deploy a bot on Nyria Paper, the free simulated broker. Each message, such as `SPY long entry`, becomes an order. Nyria fills it as a simulated order, so no real money moves. You need no webhook and no TradingView plan.

## What you need

- A Telegram group or channel you run, with the permission to add a bot.
- A free Nyria account. Nyria Paper needs no broker and no card.

## How do I set up Telegram alerts to Nyria Paper?

1. Create the account. In Nyria, select Integrations, then the Nyria Paper card, then Create Nyria Paper account. It opens with a simulated balance and needs no broker, API key or card.
2. Create a strategy. Select Create strategy and pick Telegram as the alert source. Choose stocks, options or crypto as the asset type, and set what an entry and an exit do on each side.
3. Connect Telegram. In the new strategy select Connect Telegram, press Start in the chat with @NyriaAlertsBot, then tap Link.
4. Add Nyria to the group or channel you run as an admin. It asks for one right, manage chat, and only reads.
5. Point the strategy at a channel or at its discussion group, never both. The discussion group mirrors the channel's posts, so one alert would trade twice.
6. Check a real message with the message preview before any bot is deployed.
7. Deploy a bot. Select Deploy bot, choose Nyria Paper on the Account step and set a Budget per entry. The next alert becomes a simulated order.

## What must the alert say?

Nyria needs three things from an alert: a ticker, a direction (long or short) and an action (open or close). There is no fixed template. Write the call the way a trader would: `SPY long entry`, `BTO SPY 12/18 780C`, `Close SPY long`. Case, trailing punctuation and emoji are ignored. Messages that other bots post in a group are not read, and edited messages are not traded.

## Alert messages

Each message below is a file in this folder and is read back by Nyria's alert tester through [`scripts/check_examples.py`](../../../scripts/check_examples.py). The ticker and sample values are placeholders; use your own.

### Stocks and ETFs

**Long entry.** Opens a long SPY position.

```text
SPY long entry
```

File: [`long-entry.txt`](long-entry.txt)

**Long entry, other word order.** Opens a long SPY position.

```text
long SPY here
```

File: [`long-here.txt`](long-here.txt)

**Entry with a price in the line.** Opens a long NVDA position. The number is a price in the text, not a size.

```text
NVDA long here 228
```

File: [`price-in-line.txt`](price-in-line.txt)

**Short entry.** Opens a short SPY position. Short stock needs a margin account.

```text
SPY short entry
```

File: [`short-entry.txt`](short-entry.txt)

**Exit.** Closes the SPY long.

```text
Close SPY long
```

File: [`close-long.txt`](close-long.txt)

**Exit, as a sentence.** Closes the NVDA long.

```text
Sold NVDA, closing the long
```

File: [`close-sentence.txt`](close-sentence.txt)

### Options

**Buy to open a call.** Buys to open the SPY 780 call that expires 12/18.

```text
BTO SPY 12/18 780C
```

File: [`option-bto.txt`](option-bto.txt)

**Sell to close a call.** Closes the SPY long option position.

```text
STC SPY 780c 12/18
```

File: [`option-stc.txt`](option-stc.txt)

**Buy to open with a price.** Buys to open the AAPL 345 call that expires 11/20. The order type comes from the strategy's setting.

```text
BTO AAPL 345c 11/20 @ 12.50
```

File: [`option-bto-premium.txt`](option-bto-premium.txt)

**Call spread in one line.** Buys the 780 call and sells the 785 call, both expiring 12/18, as one spread.

```text
SPY 12/18 780C/785C bull call spread
```

File: [`option-spread.txt`](option-spread.txt)

### Crypto

**Crypto entry.** Buys BTC spot.

```text
Long BTC here
```

File: [`crypto-long.txt`](crypto-long.txt)

**Crypto exit.** Sells the BTC position.

```text
Close long BTC
```

File: [`crypto-close.txt`](crypto-close.txt)

### What Nyria does not trade

**Commentary.** Refused: a message with no trade in it places no order, and the strategy logs the reason.

```text
watching TSLA into earnings, no position yet
```

File: [`not-an-alert.txt`](not-an-alert.txt)

## How do options alerts work at Nyria Paper?

Nyria Paper takes options as single legs or spreads of up to 4 legs, sent as one order. Write the contract the way the caller already does, as `BTO SPY 12/18 780C`, and set the strategy's contract selection to Provided in alert. Always include the expiration. On a Provided in alert strategy, an entry with no date uses the nearest listed expiration, which can be today's. Or set the strategy to From my rules and let its leg rules pick the contract.

## Can I trade crypto at Nyria Paper?

Nyria Paper fills crypto spot at any hour, weekends included, from the live quote. Use a strategy whose asset type is crypto. A short form such as `BTC` or `BTCUSD` works while only one selected pair matches it; if you select both the USDT and the USDC pair for a coin, the alert must name the full pair.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Undo an order by editing the message.** Editing or deleting a message after Nyria has traded on it does not reverse, change or cancel the order.

## Nyria Paper notes

- Simulated end to end: no order reaches a broker or exchange and no money moves.
- Stocks, options (single legs and spreads up to 4 legs) and crypto spot.
- A market order fills at the ask to buy and the bid to sell, from the quote Nyria read when the alert arrived. A limit order fills or is refused at once against that quote.
- Options alerts are refused while the options market is closed, and the log says so. Stocks and crypto fill at any hour.
- There is no slippage, so paper results usually read better than a live account would on the same alerts.
- Nothing queues, so there is no working order to MODIFY or CANCEL.

## Links

- [How to automate Telegram alerts to Nyria Paper](https://nyria.io/automate/telegram-to-paper): the step-by-step page on nyria.io
- [Telegram on Nyria](https://nyria.io/signals/telegram)
- [Guide: Telegram alerts to broker orders](https://nyria.io/guides/telegram-alerts-to-broker)
- [Nyria Paper on Nyria](https://docs.nyria.io/integrations/brokers/nyria-paper) and [the Nyria Paper docs](https://docs.nyria.io/integrations/brokers/nyria-paper)
- [Telegram setup in the docs](https://docs.nyria.io/alerts/telegram)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [Paper trade a TradingView strategy for free](https://nyria.io/guides/paper-trade-tradingview-strategy-free)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
