# Telegram alerts to tastytrade

To automate Telegram alerts to tastytrade, add Nyria to a Telegram group or channel you run, point a Nyria strategy at it, and connect your tastytrade account. Each message, such as `SPY long entry`, becomes an order. Nyria places the order in your tastytrade account. You need no webhook and no TradingView plan.

## What you need

- A Telegram group or channel you run, with the permission to add a bot.
- A free Nyria account and your tastytrade account. Test on paper first; live trading is from $15 a month.

## How do I set up Telegram alerts to tastytrade?

1. Connect tastytrade. In Nyria, select Integrations, then the tastytrade card. Under Live trading select Connect live account. Sign in at tastytrade and select Authorize. Nyria imports every account under the login, and you pick the one a bot trades.
2. Create a strategy. Select Create strategy and pick Telegram as the alert source. Choose stocks or options as the asset type, and set what an entry and an exit do on each side.
3. Connect Telegram. In the new strategy select Connect Telegram, press Start in the chat with @NyriaAlertsBot, then tap Link.
4. Add Nyria to the group or channel you run as an admin. It asks for one right, manage chat, and only reads.
5. Point the strategy at a channel or at its discussion group, never both. The discussion group mirrors the channel's posts, so one alert would trade twice.
6. Check a real message with the message preview before any bot is deployed.
7. Deploy a bot. Select Deploy bot, pick the tastytrade account on the Account step and set a Budget per entry. A bot on a live account needs a Nyria Pro plan, from $15 a month, or a Premium strategy you have bought. tastytrade connects live accounts only. Run the strategy on Nyria Paper first, then deploy a second bot on the tastytrade account.

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

### What Nyria does not trade

**Commentary.** Refused: a message with no trade in it places no order, and the strategy logs the reason.

```text
watching TSLA into earnings, no position yet
```

File: [`not-an-alert.txt`](not-an-alert.txt)

## How do options alerts work at tastytrade?

tastytrade takes options as single legs or spreads of up to 4 legs, sent as one order. Write the contract the way the caller already does, as `BTO SPY 12/18 780C`, and set the strategy's contract selection to Provided in alert. Always include the expiration. On a Provided in alert strategy, an entry with no date uses the nearest listed expiration, which can be today's. Or set the strategy to From my rules and let its leg rules pick the contract.

## Can I trade crypto at tastytrade?

No. Crypto trading has been disabled through tastytrade's API since 29 June 2026. A crypto alert fails the entry with a crypto unavailable notice. Use Alpaca or Nyria Paper for crypto. See the [Alpaca folder](../alpaca/README.md) and the [Nyria Paper folder](../nyria-paper/README.md) for crypto spot.

## What can an alert not do?

An alert cannot:

- **Set the size.** Each bot sizes every order from its own budget per entry. A `quantity` or `notional` key on an entry is ignored.
- **Attach a stop or target.** Nyria places market and limit orders only. It sends no stop, bracket, OCO or trailing order to the broker. Exits come from your exit alerts.
- **Close part of a position.** A close closes the whole open position.
- **Undo an order by editing the message.** Editing or deleting a message after Nyria has traded on it does not reverse, change or cancel the order.
- **Trade crypto at tastytrade.** tastytrade does not carry crypto through Nyria. Use Alpaca or Nyria Paper.

## tastytrade notes

- Live accounts only, connected through tastytrade's own sign-in. The password goes to tastytrade and never to Nyria.
- Market and limit orders. A spread goes as one order for all its legs, priced as a net debit or credit when it is a limit order.
- Day and Good till canceled go to tastytrade as set. tastytrade has no fill or kill, so a strategy set to Fill or kill sends Day.
- Stocks in whole shares and options in whole contracts. Defined-risk spreads need options level 3 or higher at tastytrade.
- Crypto trading has been disabled through tastytrade's API since 29 June 2026. A crypto alert fails the entry with a crypto unavailable notice. Use Alpaca or Nyria Paper for crypto.
- MODIFY is refused at tastytrade. To re-price a resting entry, send CANCEL, then a new OPEN.

## Links

- [How to automate Telegram alerts to tastytrade](https://nyria.io/automate/telegram-to-tastytrade): the step-by-step page on nyria.io
- [Telegram on Nyria](https://nyria.io/signals/telegram)
- [Guide: Telegram alerts to broker orders](https://nyria.io/guides/telegram-alerts-to-broker)
- [tastytrade on Nyria](https://nyria.io/integrations/tastytrade) and [the tastytrade docs](https://docs.nyria.io/integrations/brokers/tastytrade)
- [Telegram setup in the docs](https://docs.nyria.io/alerts/telegram)
- [Alert tester](https://nyria.io/tools/alert-tester): paste an alert and read the order Nyria would send. Nothing is traded and no account is needed.
- [Webhook payload reference](https://docs.nyria.io/webhook-reference)
- [FAQ](../../../FAQ.md)

Nothing here is financial advice, and an automated order can lose money. Read the [risk disclosure](https://docs.nyria.io/risk-disclosure) and run every new alert on paper first.
