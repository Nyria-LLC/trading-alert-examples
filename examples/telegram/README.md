# Telegram alerts to a broker

Nyria reads the messages in one Telegram group or channel that you run, and each bot on the strategy places the order in its own account: Charles Schwab, Tradier, tastytrade, Alpaca or Nyria Paper, the free simulated broker. A caller types a sentence or a short line of notation. There is no template, no webhook and no TradingView plan.

An alert needs three things: a ticker, a direction (long or short) and an action (open or close). Case, trailing punctuation, emoji and `@everyone` are ignored. The message never sets the size; each bot sizes the order from its own budget per entry.

## Pick your broker

| Broker | Messages and setup |
|---|---|
| Charles Schwab | [Telegram alerts to Charles Schwab](schwab/README.md) |
| Tradier | [Telegram alerts to Tradier](tradier/README.md) |
| tastytrade | [Telegram alerts to tastytrade](tastytrade/README.md) |
| Alpaca | [Telegram alerts to Alpaca](alpaca/README.md), with crypto |
| Nyria Paper | [Telegram alerts to Nyria Paper](nyria-paper/README.md), with crypto |

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

## How do I point Nyria at the chat?

1. In a new strategy pick Telegram and select Connect Telegram. Press Start in the chat with @NyriaAlertsBot, then tap Link.
2. Add Nyria to the group or channel as an admin. It asks for one right, manage chat, and only reads.
3. Point the strategy at a channel or at its discussion group, never both, because the discussion group mirrors the channel's posts and one alert would trade twice.
4. Validate with the message preview, then deploy on Nyria Paper first.

- [How to automate Telegram alerts, step by step](https://nyria.io/guides/telegram-alerts-to-broker)
- [Telegram alerts on Nyria](https://nyria.io/signals/telegram)
- [Trade alerts from a Telegram chat you run](https://docs.nyria.io/alerts/telegram)

## Links

An edited Telegram message places no order; post a new one. An alert that reaches Nyria more than a minute after it was posted, or after a newer one, places no new entry. A close in it still runs. Messages that other bots post in a group are not read, and messages posted before Nyria joined the chat cannot be read.
- [Alert tester](https://nyria.io/tools/alert-tester): paste a message and read the order Nyria would send.
