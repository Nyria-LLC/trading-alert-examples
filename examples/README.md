# Examples

One folder for each alert source and broker pair. Each folder holds a README that answers one question, for example "how do I automate TradingView alerts to Charles Schwab?", and the alert files it shows. Every file is read back by Nyria's alert tester through [`../scripts/check_examples.py`](../scripts/check_examples.py).

```text
examples/<source>/<broker>/README.md
examples/<source>/<broker>/*.json | *.txt
```

| Source | Charles Schwab | Tradier | tastytrade | Alpaca | Nyria Paper |
|---|---|---|---|---|---|
| [TradingView](tradingview/README.md) | [open](tradingview/schwab/README.md) | [open](tradingview/tradier/README.md) | [open](tradingview/tastytrade/README.md) | [open](tradingview/alpaca/README.md) | [open](tradingview/nyria-paper/README.md) |
| [TrendSpider](trendspider/README.md) | [open](trendspider/schwab/README.md) | [open](trendspider/tradier/README.md) | [open](trendspider/tastytrade/README.md) | [open](trendspider/alpaca/README.md) | [open](trendspider/nyria-paper/README.md) |
| [Discord](discord/README.md) | [open](discord/schwab/README.md) | [open](discord/tradier/README.md) | [open](discord/tastytrade/README.md) | [open](discord/alpaca/README.md) | [open](discord/nyria-paper/README.md) |
| [Telegram](telegram/README.md) | [open](telegram/schwab/README.md) | [open](telegram/tradier/README.md) | [open](telegram/tastytrade/README.md) | [open](telegram/alpaca/README.md) | [open](telegram/nyria-paper/README.md) |
| [Webhook](webhook/README.md) | [open](webhook/schwab/README.md) | [open](webhook/tradier/README.md) | [open](webhook/tastytrade/README.md) | [open](webhook/alpaca/README.md) | [open](webhook/nyria-paper/README.md) |
| [Python](python/README.md) | [open](python/schwab/README.md) | [open](python/tradier/README.md) | [open](python/tastytrade/README.md) | [open](python/alpaca/README.md) | [open](python/nyria-paper/README.md) |

The alert does not change with the broker. A message that works for Schwab works for Tradier, tastytrade, Alpaca and Nyria Paper, because the bot you deploy decides where the order goes. The broker folders differ in how the broker connects, which assets it carries and what it refuses:

- Crypto spot files exist for Alpaca and Nyria Paper only. Schwab, Tradier and tastytrade do not carry crypto through Nyria.
- `MODIFY` re-prices a resting limit order at Tradier and Alpaca. Schwab and tastytrade refuse it.
- Nyria Paper refuses options alerts while the options market is closed.

Shared files: [`tradingview/pine`](tradingview/pine) holds the Pine Script v6 examples, [`webhook`](webhook) holds the curl and Node senders, and [`python`](python) holds the Python sender.
