# Discord alerts to Tradier

To automate Discord alerts to Tradier, invite the Nyria bot to a Discord server you run, pick the alerts channel in a Nyria strategy, and connect your Tradier account. Each call posted in that channel, such as `SPY long entry`, becomes an order. Nyria places the order in your Tradier account. You need no webhook and no TradingView plan.

## What you need

- A Discord server you run, with the permission to add a bot.
- A free Nyria account and your Tradier account. Test on paper first; live trading is from $15 a month.

## How do I set up Discord alerts to Tradier?

1. Connect Tradier. In Nyria, select Integrations, then the Tradier card, then Connect live account, and approve access on Tradier's own screen. For Tradier's sandbox instead, select Connect paper account and paste the sandbox account number and access token from developer.tradier.com. The sandbox is a separate account from the live one, so the same strategy can run on both.
2. Create a strategy. Select Create strategy and pick Discord as the alert source. Choose stocks or options as the asset type, and set what an entry and an exit do on each side.
3. Link Discord. Under Integrations open the Discord card and select Connect Discord. Nyria asks Discord only for your identity and server list.
4. Invite the bot. On the strategy's Discord channel step select Invite bot to server. You need the Manage Server permission on a server you run. The bot asks for one permission, View Channels, and only reads.
5. Choose one channel. Threads, other channels and direct messages are not read. Add an author or keyword filter if others post there.
6. Assign a real message from the channel to each side the strategy uses, such as Long entry and Long exit, and check what Nyria parsed.
7. Deploy a bot. Select Deploy bot, pick the Tradier account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. Tradier's sandbox connects as a paper account, and Nyria Paper works too.

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

### What Nyria does not trade

**Commentary.** Refused: a message with no trade in it places no order, and the strategy logs the reason.

```text
watching TSLA into earnings, no position yet
```

File: [`not-an-alert.txt`](not-an-alert.txt)

## How do options alerts work at Tradier?

Tradier takes options as single legs or spreads of up to 4 legs, sent as one order. Write the contract the way the caller already does, as `BTO SPY 12/18 780C`, and set the strategy's contract selection to Provided in alert. Always include the expiration. On a Provided in alert strategy, an entry with no date uses the nearest listed expiration, which can be today's. Or set the strategy to From my rules and let its leg rules pick the contract.

## Can I trade crypto at Tradier?

No. Tradier does not offer crypto, so a crypto alert places no order there. Use Alpaca or Nyria Paper for crypto. See the [Alpaca folder](../alpaca/README.md) and the [Nyria Paper folder](../nyria-paper/README.md) for crypto spot.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Undo an order by editing the message.** Editing or deleting a message after Nyria has traded on it does not reverse, change or cancel the order.
- **Trade crypto at Tradier.** Tradier does not carry crypto through Nyria. Use Alpaca or Nyria Paper.

## Tradier notes

- Live accounts connect through Tradier's sign-in. Paper uses Tradier Sandbox credentials.
- Market and limit orders, for entries and exits. A spread goes as one order for all its legs.
- Day and Good till canceled go to Tradier as set. Tradier has no fill or kill, so a strategy set to Fill or kill sends Day.
- No fractional shares, and options in whole contracts.
- Tradier restricts market orders outside regular hours. Turn on Limit trading hours on the strategy to keep entries inside them.
- Short stock and short spreads need a margin account and the options level the trade requires.
- Tradier does not offer crypto, so a crypto alert places no order there. Use Alpaca or Nyria Paper for crypto.
- MODIFY works at Tradier, so a resting limit entry can be re-priced with a second alert.

## Links

- [How to automate Discord alerts to Tradier](https://nyria.io/automate/discord-to-tradier): the step-by-step page on nyria.io
- [Discord on Nyria](https://nyria.io/signals/discord)
- [Guide: Discord alerts to broker orders](https://nyria.io/guides/discord-alerts-to-broker)
- [Tradier on Nyria](https://nyria.io/integrations/tradier) and [the Tradier docs](https://docs.nyria.io/integrations/brokers/tradier)
- [Discord setup in the docs](https://docs.nyria.io/alerts/discord)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
