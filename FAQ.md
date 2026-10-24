# FAQ

Short answers to the questions traders ask most about automating alerts. Each links to the longer nyria.io page.

## How do I automate TradingView alerts to a broker?

Create a Nyria strategy with TradingView as the alert source, connect Charles Schwab, Tradier, tastytrade, Alpaca or the free Nyria Paper simulator, and paste the strategy's webhook URL into the alert's Webhook URL box. The message names a ticker, a side and whether it opens or closes. Nyria places the order in your account. Steps: [Automate TradingView alerts](https://nyria.io/guides/automate-tradingview-alerts). Messages to copy: [examples/tradingview](examples/tradingview/README.md).

## Can I use TradingView webhook alerts for free?

Only partly. TradingView sends webhooks on its paid plans only, with two-factor sign-in on, so the sending side is not free. The receiving side is: Nyria Paper is a simulated broker with up to 10 paper bots, no card and no time limit. Live trading at your own broker is from $15 a month. A call posted in a Discord server or Telegram chat you run needs no TradingView plan. More: [Free TradingView webhook alerts](https://nyria.io/guides/free-tradingview-webhook-alerts).

## What JSON format does a TradingView webhook need?

None in particular. TradingView posts the Message box as written: valid JSON goes out as `application/json` and anything else as `text/plain`. Nyria reads either one. The message has to name the ticker, the side and whether it opens or closes, and `AAPL long entry` is enough. More: [TradingView webhook JSON format](https://nyria.io/guides/tradingview-webhook-json-format). Examples: [strategy-order-fills.json](examples/tradingview/schwab/strategy-order-fills.json) and [indicator-long-entry.json](examples/tradingview/schwab/indicator-long-entry.json).

## Can TradingView send a webhook to localhost, and do I need a server?

No to localhost: TradingView posts from its own servers, which cannot reach an address on your machine, and it accepts only ports 80 and 443. You need no server with Nyria. Each strategy has a hosted webhook URL at `trades.nyria.io`, so there is nothing to run, tunnel or allowlist. More: [TradingView webhook without localhost](https://nyria.io/guides/tradingview-webhook-without-localhost).

## Which IP addresses does TradingView send webhooks from?

TradingView's help page lists four: 52.89.214.238, 34.212.75.30, 54.218.53.128 and 52.32.178.7. The list can change, so check that page before you rely on it. Allowlisting only matters on a server you run; with a hosted Nyria URL there is nothing to allowlist. More: [TradingView webhook IP addresses](https://nyria.io/guides/tradingview-webhook-ip-address).

## Why is my TradingView alert not firing?

Usually it expired, its condition was not true when the trigger checked, or it hit a TradingView limit. Check the expiration, the trigger, the condition, the script and the alert log, in that order. If the alert fires and no order follows, the fault is in the webhook or the bot. More: [Why is my TradingView alert not firing?](https://nyria.io/guides/tradingview-alerts-not-firing) and [TradingView webhook not working: a checklist](https://nyria.io/guides/tradingview-webhook-not-working).

## Do I have to code against the Schwab API to automate trades?

No. Charles Schwab, Tradier, tastytrade and Alpaca publish APIs that take orders, but something still has to read your alerts and place them. Nyria is that part, with no code to write: Schwab, Tradier and tastytrade connect through the broker's own sign-in and Alpaca with an API key. More: [Broker API trading](https://nyria.io/guides/broker-api-trading) and [TradingView alerts to Schwab](https://nyria.io/automate/tradingview-to-schwab).

## Can an alert trade options and multi-leg spreads?

Yes, up to 4 legs on one expiration, sent to the broker as one order. For TradingView the strategy's leg rules pick the contract and the alert says the direction. With Discord, Telegram or your own code the alert can name the strike and expiration. Calendars, diagonals and ratio spreads cannot be built. More: [Multi-leg options strategies](https://docs.nyria.io/strategies/multi-leg-options). Files: [examples/webhook/schwab](examples/webhook/schwab/README.md).

## Can an alert set the order size or attach a stop loss?

No to both. Each bot sizes every order from its own budget per entry, and a `quantity` or `notional` key is ignored. Nyria places market and limit orders only, with no stop, bracket, OCO or trailing order, so exits come from your exit alerts. More: [Known limitations](https://docs.nyria.io/limitations) and the [webhook payload reference](https://docs.nyria.io/webhook-reference).

## How do I test an automated strategy without risking money?

Send the real alerts to a bot on Nyria Paper. It is free, needs no broker and fills from the live quote. Read every order on the Logs tab against the alert that caused it. Paper fills never slip, so a live account can fill at a worse price. When the log matches what you meant, go live with a small budget per entry. More: [Paper trade a TradingView strategy for free](https://nyria.io/guides/paper-trade-tradingview-strategy-free).

## Can alerts trade crypto?

At Alpaca and on Nyria Paper, as spot. Schwab and Tradier do not carry crypto, and tastytrade disabled crypto in its API on 29 June 2026. More: [Alpaca automated trading](https://nyria.io/guides/alpaca-automated-trading). Files: [examples/webhook/alpaca](examples/webhook/alpaca/README.md).

## Is automated trading profitable?

It depends on the rules, not on the automation. A bot places the orders your rules describe, the same way each time, and it makes a weak rule no better. Any strategy can lose money, and Nyria publishes no performance figures. Run the rule on paper, read every fill, then go live small and check each fill against your broker's history. More: [Is automated trading profitable?](https://nyria.io/guides/is-automated-trading-profitable).
