# Discord and Telegram

Nyria reads the messages in one Discord channel or one Telegram group or channel that you run, and each bot on the strategy places the order in its own account. A caller types a sentence or a short line of notation. There is no template.

An alert needs three things: a ticker, a direction (long or short) and an action (open or close). Case, trailing punctuation, emoji and `@everyone` are ignored. The message never sets the size; each bot sizes the order from its own budget per entry.

Every message below is listed in [`../alerts.json`](../alerts.json) and read back by Nyria's alert tester through [`../scripts/check_examples.py`](../scripts/check_examples.py).

## Stocks and ETFs

| Message | Read as |
|---|---|
| `long SPY here` | Open a long SPY position |
| `SPY long entry` | Open a long SPY position |
| `NVDA long here 228` | Open a long NVDA position; the number is a price in the text, not a size |
| `SPY short entry` | Open a short SPY position |
| `Close SPY long` | Close the SPY long |
| `Sold NVDA, closing the long` | Close the NVDA long |

## Options

An options line names the contract: underlying, expiration, strike and call or put. Write the expiration as a date that exists. These dates are examples; change them to a current expiration.

| Message | Read as |
|---|---|
| `BTO SPY 12/18 780C` | Buy to open the SPY 780 call that expires 12/18 |
| `STC SPY 780c 12/18` | Sell to close, which closes the SPY long option position |
| `BTO AAPL 345c 11/20 @ 12.50` | Buy to open the AAPL 345 call that expires 11/20 |

`BTO` is buy to open and `STC` is sell to close. The tester reads the order from the line and shows a market order for each of these; the order type of a chat alert comes from the strategy's setting.

## Crypto

| Message | Read as |
|---|---|
| `Long BTC here` | Buy BTC spot |

## What Nyria does not trade

A message with no trade in it is refused, and the strategy logs the reason.

| Message | Result |
|---|---|
| `watching TSLA into earnings, no position yet` | Refused: Nyria found no trade in this message. An alert needs an action (open or close) and a direction (long or short). |

## Point Nyria at the channel

Discord:

1. Link Discord under Integrations and invite the Nyria bot to a server you run. You need the Manage Server permission. The invite asks for one permission, View Channels, and the bot only reads.
2. Create a strategy, pick Discord as the alert source and choose one channel. Threads, other channels and direct messages are not read.
3. Optionally add an author filter (part of the poster's display name) or a keyword filter.
4. Assign a real message from the preview to Long entry, Long exit, Short entry or Short exit and check what Nyria parsed.
5. Deploy a bot on Nyria Paper and let a real call fire before any live account sees it.

Editing or deleting a message after Nyria has traded on it does not reverse, change or cancel the order.

Telegram:

1. In a new strategy pick Telegram and select Connect Telegram. Press Start in the chat with @NyriaAlertsBot, then tap Link.
2. Add Nyria to the group or channel as an admin. It asks for one right, manage chat, and only reads.
3. Point the strategy at a channel or at its discussion group, never both, because the discussion group mirrors the channel's posts and one alert would trade twice.
4. Validate with the message preview, then deploy on Nyria Paper first.

An edited Telegram message places no order; post a new one. An alert that reaches Nyria more than a minute after it was posted, or after a newer one, places no new entry. A close in it still runs.

## Links

- [How to automate Discord alerts, step by step](https://nyria.io/guides/discord-alerts-to-broker)
- [How to automate Telegram alerts, step by step](https://nyria.io/guides/telegram-alerts-to-broker)
- [Alert tester](https://nyria.io/tools/alert-tester): paste a message and read the order Nyria would send.
- [Discord alerts to Alpaca](https://nyria.io/automate/discord-to-alpaca) and [Telegram alerts to Alpaca](https://nyria.io/automate/telegram-to-alpaca); Charles Schwab, Tradier and tastytrade have matching pages under [nyria.io/automate](https://nyria.io/automate).
- [Discord](https://docs.nyria.io/alerts/discord) and [Telegram](https://docs.nyria.io/alerts/telegram) in the docs
