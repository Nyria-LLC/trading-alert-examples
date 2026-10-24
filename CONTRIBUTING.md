# Contributing

Fixes and new examples are welcome. The rule is simple: an example here is read by Nyria's alert tester the way its README says it is.

## Report a problem

Open an issue with the example id from [`alerts.json`](alerts.json) or the file path, and paste what the [alert tester](https://nyria.io/tools/alert-tester) shows. Never paste a webhook URL or token. If one was posted by mistake, rotate the token on the strategy's Integration tab.

## Add or change an example

1. Put the alert in the folder for its source and broker, for example `examples/discord/alpaca/`. A file holds one alert. Use `.json` for a JSON body and `.txt` for a line of text.
2. Add it to the folder's `README.md`, with the text verbatim in a code block and one line saying what it reads as.
3. Add an entry to `alerts.json`: an `id`, the tester `source` (`tradingview`, `discord`, `telegram` or `webhook`), the `asset` (`stocks`, `options` or `crypto`), the `files` that hold the alert (every broker folder that shows it), and the reading it must produce under `expect`. Options also take a `contract`: `delta` for "From my rules" and `alert` for "Provided in alert". TradingView placeholders such as `{{ticker}}` and TrendSpider variables such as `%alert_symbol%` are filled with sample values; add a `sample` to override one.
4. Run the checker:

```sh
python3 scripts/check_examples.py --offline                 # files, READMEs and dates
python3 scripts/check_examples.py --only discord/option-bto # one example against the tester
```

The checker needs only the Python 3 standard library. The tester is rate limited, so run the full set sparingly.

## Keep it true

- Do not claim a feature Nyria lacks. An alert cannot set the order size, and Nyria attaches no stop or target. Check the [docs](https://docs.nyria.io) first.
- Options need an expiration that exists. The checker fails an example whose date has passed.
- Say what an example does, not what it earns. No performance claims.
- Plain, short sentences. No marketing copy.

By contributing you agree that your work is released under the [MIT license](LICENSE).
