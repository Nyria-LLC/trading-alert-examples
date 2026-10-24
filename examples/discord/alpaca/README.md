# Discord alerts to Alpaca

To automate Discord alerts to Alpaca, invite the Nyria bot to a Discord server you run, pick the alerts channel in a Nyria strategy, and connect your Alpaca account. Each call posted in that channel, such as `SPY long entry`, becomes an order. Nyria places the order in your Alpaca account. You need no webhook and no TradingView plan.

## What you need

- A Discord server you run, with the permission to add a bot.
- A free Nyria account and your Alpaca account. Test on paper first; live trading is from $15 a month.

## How do I set up Discord alerts to Alpaca?

1. Connect Alpaca. In the Alpaca dashboard, switch to Paper or Live and select Generate New Keys. Copy the API key ID and the secret key; Alpaca shows the secret once. Give the key trading permission only. In Nyria, select Integrations, then the Alpaca card, then Connect paper account or Connect live account. Select Accept and continue and paste both values. A paper key works only on paper and a live key only on live, so the same strategy can run on both.
2. Create a strategy. Select Create strategy and pick Discord as the alert source. Choose stocks, options or crypto as the asset type, and set what an entry and an exit do on each side.
3. Link Discord. Under Integrations open the Discord card and select Connect Discord. Nyria asks Discord only for your identity and server list.
4. Invite the bot. On the strategy's Discord channel step select Invite bot to server. You need the Manage Server permission on a server you run. The bot asks for one permission, View Channels, and only reads.
5. Choose one channel. Threads, other channels and direct messages are not read. Add an author or keyword filter if others post there.
6. Assign a real message from the channel to each side the strategy uses, such as Long entry and Long exit, and check what Nyria parsed.
7. Deploy a bot. Select Deploy bot, pick the Alpaca account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. An Alpaca paper account connects the same way as a live one, and Nyria Paper works too.

## What must the alert say?

Nyria needs three things from an alert: a ticker, a direction (long or short) and an action (open or close). There is no fixed template. Write the call the way a trader would: `SPY long entry`, `BTO SPY 12/18 780C`, `Close SPY long`. Case, trailing punctuation, emoji and `@everyone` are ignored. Nyria reads one channel, from any member, bot or webhook, and does not read edits.

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

## How do options alerts work at Alpaca?

Alpaca takes options as single legs or spreads of up to 4 legs, sent as one order. Write the contract the way the caller already does, as `BTO SPY 12/18 780C`, and set the strategy's contract selection to Provided in alert. Always include the expiration. On a Provided in alert strategy, an entry with no date uses the nearest listed expiration, which can be today's. Or set the strategy to From my rules and let its leg rules pick the contract.

## Can I trade crypto at Alpaca?

Alpaca trades crypto spot in the pairs it lists. Crypto orders go to Alpaca as good till canceled, and positions are fractional. Use a strategy whose asset type is crypto. A short form such as `BTC` or `BTCUSD` works while only one selected pair matches it; if you select both the USDT and the USDC pair for a coin, the alert must name the full pair.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Undo an order by editing the message.** Editing or deleting a message after Nyria has traded on it does not reverse, change or cancel the order.

## Alpaca notes

- Alpaca connects with an API key, not a sign-in. Nyria stores the key encrypted at rest.
- Stocks, options up to 4 legs and crypto spot. Options trading must be turned on in the Alpaca account.
- Market and limit orders. Stock orders take the strategy's Duration as set. Option orders go to Alpaca as Day, and crypto orders as Good till canceled.
- Stocks in whole shares. Crypto trades in fractions, so a $100 entry with BTC at $64,000 buys 0.00156 BTC.
- US equities only. Alpaca restricts some order types outside market hours; turn on Limit trading hours on the strategy to keep entries inside them.
- MODIFY works at Alpaca, so a resting limit entry can be re-priced with a second alert.

## Links

- [How to automate Discord alerts to Alpaca](https://nyria.io/automate/discord-to-alpaca): the step-by-step page on nyria.io
- [Discord on Nyria](https://nyria.io/signals/discord)
- [Guide: Discord alerts to broker orders](https://nyria.io/guides/discord-alerts-to-broker)
- [Alpaca on Nyria](https://nyria.io/integrations/alpaca) and [the Alpaca docs](https://docs.nyria.io/integrations/brokers/alpaca)
- [Discord setup in the docs](https://docs.nyria.io/alerts/discord)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
