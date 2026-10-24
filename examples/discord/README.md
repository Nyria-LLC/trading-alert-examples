# Discord alerts to a broker

Nyria reads the messages in one Discord channel that you run, and each bot on the strategy places the order in its own account: Charles Schwab, Tradier, tastytrade, Alpaca or Nyria Paper, the free simulated broker. A caller types a sentence or a short line of notation. There is no template, no webhook and no TradingView plan.

An alert needs three things: a ticker, a direction (long or short) and an action (open or close). Case, trailing punctuation, emoji and `@everyone` are ignored. The message never sets the size; each bot sizes the order from its own budget per entry.

## Pick your broker

| Broker | Messages and setup |
|---|---|
| Charles Schwab | [Discord alerts to Charles Schwab](schwab/README.md) |
| Tradier | [Discord alerts to Tradier](tradier/README.md) |
| tastytrade | [Discord alerts to tastytrade](tastytrade/README.md) |
| Alpaca | [Discord alerts to Alpaca](alpaca/README.md), with crypto |
| Nyria Paper | [Discord alerts to Nyria Paper](nyria-paper/README.md), with crypto |

The message does not change with the broker. Every line is read back by Nyria's alert tester through [`../../scripts/check_examples.py`](../../scripts/check_examples.py).

## Which messages are read?

| Message | Read as |
|---|---|
| `long SPY here` | Open a long SPY position |
| `SPY long entry` | Open a long SPY position |
| `NVDA long here 228` | Open a long NVDA position; the number is a price in the text, not a size |
| `SPY short entry` | Open a short SPY position |
| `Close SPY long` | Close the SPY long |
| `Sold NVDA, closing the long` | Close the NVDA long |
| `BTO SPY 12/18 780C` | Buy to open the SPY 780 call that expires 12/18 |
| `STC SPY 780c 12/18` | Sell to close, which closes the SPY long option position |
| `Long BTC here` | Buy BTC spot (Alpaca and Nyria Paper) |
| `watching TSLA into earnings, no position yet` | Refused: it holds no trade |

`BTO` is buy to open and `STC` is sell to close. Write an options expiration as a date that exists; the dates in these files are examples, so change them to a current expiration. On a "Provided in alert" strategy, an options entry with no date uses the nearest listed expiration, which can be today's.

## How do I point Nyria at the channel?

1. Link Discord under Integrations and invite the Nyria bot to a server you run. You need the Manage Server permission. The invite asks for one permission, View Channels, and the bot only reads.
2. Create a strategy, pick Discord as the alert source and choose one channel. Threads, other channels and direct messages are not read.
3. Optionally add an author filter (part of the poster's display name) or a keyword filter.
4. Assign a real message from the preview to Long entry, Long exit, Short entry or Short exit and check what Nyria parsed.
5. Deploy a bot on Nyria Paper and let a real call fire before any live account sees it.

- [How to automate Discord alerts, step by step](https://nyria.io/guides/discord-alerts-to-broker)
- [Discord alerts on Nyria](https://nyria.io/signals/discord)
- [Trade alerts from a Discord server you run](https://docs.nyria.io/alerts/discord)

## Links

Editing or deleting a message after Nyria has traded on it does not reverse, change or cancel the order. A caller who changes their display name stops matching the author filter.
- [Alert tester](https://nyria.io/tools/alert-tester): paste a message and read the order Nyria would send.
