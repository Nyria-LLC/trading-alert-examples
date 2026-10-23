#!/usr/bin/env python3
"""Check every alert example in this repository against Nyria's public alert tester.

The tester (POST https://api.nyria.io/public/alert-tester) runs the parser's own
validation step on a pasted alert against a private strategy. It never places an
order and needs no account.

Each entry in alerts.json names one alert, the source and asset type to test it
under, and the reading it must produce. The script:

  1. loads the alert text (inline "text", or the contents of "file"),
  2. checks that the text appears verbatim in every file listed in "also_in",
  3. fills TradingView placeholders such as {{ticker}} with sample values,
  4. asks the tester to read it and compares the reading with "expect".

Exit status is 0 only when every selected example matches.

Usage:
  python3 scripts/check_examples.py                 # all examples
  python3 scripts/check_examples.py --only tv-json-open-long
  python3 scripts/check_examples.py --offline       # file checks only, no network
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "alerts.json"
ENDPOINT = "https://api.nyria.io/public/alert-tester"
MAX_ALERT_CHARS = 2000

# Values TradingView would fill in. Placeholders that are not listed are left
# as written, which is what TradingView does with a name it does not know.
DEFAULT_SAMPLE = {
    "ticker": "SPY",
    "close": "640.5",
    "strategy.order.action": "buy",
    "strategy.order.contracts": "1",
    "strategy.market_position": "long",
    "strategy.prev_market_position": "flat",
}

TRANSIENT_CODES = {"AI_UNAVAILABLE", "UNAVAILABLE"}
MAX_WAIT = 90  # longest Retry-After, in seconds, the script will sit through


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def fill_placeholders(text: str, sample: dict[str, str]) -> str:
    values = {**DEFAULT_SAMPLE, **sample}
    return re.sub(r"\{\{([a-z_.]+)\}\}", lambda m: values.get(m.group(1), m.group(0)), text)


def load_text(entry: dict) -> str:
    if "file" in entry:
        return (ROOT / entry["file"]).read_text().strip()
    return entry["text"]


def stale_dates(text: str, today: dt.date) -> list[str]:
    """Dates in the alert that are already in the past: 2026-12-18, or a bare 12/18 this year."""
    out = []
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        try:
            if dt.date(int(m[1]), int(m[2]), int(m[3])) < today:
                out.append(m[0])
        except ValueError:
            out.append(m[0])
    for m in re.finditer(r"(?<![\w/.])(\d{1,2})/(\d{1,2})(?![\w/.])", text):
        month, day = int(m[1]), int(m[2])
        if 1 <= month <= 12 and 1 <= day <= 31:
            try:
                if dt.date(today.year, month, day) < today:
                    out.append(m[0])
            except ValueError:
                out.append(m[0])
    return out


def ask(text: str, entry: dict, pace: float, retries: int = 2) -> tuple[dict, int]:
    body = {"text": text, "source": entry["source"], "asset": entry["asset"]}
    if entry["asset"] == "options":
        body["contract"] = entry.get("contract", "alert")
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json", "x-csrf-token": "orpc", "User-Agent": "trading-alert-examples-check/1"}
    status, answer = 0, {}
    for attempt in range(retries + 1):
        req = urllib.request.Request(ENDPOINT, data, headers, method="POST")
        wait = pace
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                status, answer = r.status, json.load(r)
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                answer = json.loads(e.read() or b"{}")
            except ValueError:
                answer = {}
            if status == 429:
                wait = float(e.headers.get("Retry-After") or 20)
                if wait > MAX_WAIT:
                    # Retrying inside a long penalty window only extends it.
                    answer = {"ok": False, "refusal": {"code": "RATE_LIMITED_LONG", "message": f"the tester asks for {int(wait)} seconds; rerun later or use --only"}}
                    return answer, status
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            answer = {"ok": False, "refusal": {"code": "NETWORK", "message": str(e)}}
            wait = 10
        code = (answer.get("refusal") or {}).get("code")
        if status == 429 or code in TRANSIENT_CODES or code == "NETWORK":
            if attempt < retries:
                time.sleep(max(wait, 15))
                continue
        else:
            time.sleep(pace)
        break
    return answer, status


def describe(reading: dict) -> str:
    legs = "; ".join(f'{l["action"]} {l["side"]} {l["strike"]} {l["expiration"]}' for l in reading.get("legs", []))
    pick = reading.get("contract") or {}
    picks = ""
    if pick.get("picksBy") == "delta":
        picks = f' delta={pick["delta"]} dte={pick["dteMin"]}-{pick["dteMax"]}'
    elif pick.get("picksBy") == "alert":
        picks = " contract=from alert"
    s = f'{reading["action"]} {reading["direction"]} {reading["instrument"]} ({reading["asset"]}, {reading["orderType"]})'
    return s + (f" legs=[{legs}]" if legs else "") + picks


def compare(reading: dict, expect: dict) -> list[str]:
    problems = []
    for key in ("action", "direction", "instrument", "asset", "orderType", "identifier"):
        if key in expect and reading.get(key) != expect[key]:
            problems.append(f"{key}: expected {expect[key]!r}, read {reading.get(key)!r}")
    if "legs" in expect:
        got = [[l["action"], l["side"], l["strike"]] for l in reading.get("legs", [])]
        if got != expect["legs"]:
            problems.append(f"legs: expected {expect['legs']}, read {got}")
    if "picksBy" in expect and (reading.get("contract") or {}).get("picksBy") != expect["picksBy"]:
        problems.append(f"picksBy: expected {expect['picksBy']!r}, read {(reading.get('contract') or {}).get('picksBy')!r}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", default=[], help="check only this example id (repeatable)")
    ap.add_argument("--offline", action="store_true", help="verify files and dates only; skip the tester")
    ap.add_argument("--pace", type=float, default=6.0, help="seconds between requests (default 6)")
    args = ap.parse_args()

    entries = json.loads(MANIFEST.read_text())
    ids = [e["id"] for e in entries]
    if len(set(ids)) != len(ids):
        print("alerts.json has duplicate ids", file=sys.stderr)
        return 2
    unknown = [i for i in args.only if i not in ids]
    if unknown:
        print(f"unknown id: {', '.join(unknown)}", file=sys.stderr)
        return 2
    selected = [e for e in entries if not args.only or e["id"] in args.only]

    today = dt.date.today()
    failures = 0
    checked = 0
    for e in selected:
        text = load_text(e)
        problems: list[str] = []
        for path in e.get("also_in", []):
            haystack = normalize((ROOT / path).read_text())
            if normalize(text) not in haystack:
                problems.append(f"text not found verbatim in {path}")
        if len(text) > MAX_ALERT_CHARS:
            problems.append(f"{len(text)} characters; the tester accepts {MAX_ALERT_CHARS}")
        old = stale_dates(text, today)
        if old:
            problems.append(f"expiry already passed: {', '.join(old)}; pick a current expiration")

        line = ""
        if not problems and not args.offline:
            answer, status = ask(fill_placeholders(text, e.get("sample", {})), e, args.pace)
            expect = e["expect"]
            if answer.get("ok"):
                reading = answer["reading"]
                if "refusal" in expect:
                    problems.append(f"expected refusal {expect['refusal']}, but it was read: {describe(reading)}")
                else:
                    problems += compare(reading, expect)
                line = describe(reading)
            else:
                refusal = answer.get("refusal") or {}
                code = refusal.get("code", f"HTTP {status}")
                if code == "RATE_LIMITED_LONG":
                    print(f"STOP {e['id']}: {refusal['message']}")
                    print(f"\n{checked} of {len(selected)} examples checked before the stop; {checked - failures} matched")
                    return 3
                if expect.get("refusal") == code:
                    line = f"refused as expected ({code})"
                else:
                    problems.append(f"refused with {code}: {refusal.get('message') or answer.get('message') or 'no message'}")
        elif args.offline and not problems:
            line = "files ok (tester skipped)"

        checked += 1
        if problems:
            failures += 1
            print(f"FAIL {e['id']}  [{e['source']}/{e['asset']}]")
            for p in problems:
                print(f"       {p}")
        else:
            print(f"ok   {e['id']}  [{e['source']}/{e['asset']}] -> {line}")

    print(f"\n{len(selected) - failures}/{len(selected)} examples match")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
