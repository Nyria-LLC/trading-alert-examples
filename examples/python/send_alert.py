#!/usr/bin/env python3
"""Post one alert body to a Nyria strategy webhook with requests.

    export NYRIA_WEBHOOK_URL='https://trades.nyria.io/webhooks/<your-strategy-token>'
    python3 send_alert.py schwab/stock-open-long.json
    python3 send_alert.py alpaca/crypto-open-long.json

A .txt file goes as text/plain and anything else as application/json.

Exit status is 0 only when Nyria answers {"status": "processed"}. A 200 can also carry a
rejection or a duplicate, so the body is checked as well as the status code. A 200 means the
alert was read and handed to the bots on the strategy; it does not mean the broker filled it.
"""

import json
import os
import sys
from pathlib import Path

import requests

url = os.environ.get("NYRIA_WEBHOOK_URL")
if not url:
    sys.exit("Set NYRIA_WEBHOOK_URL to the webhook URL from the strategy's Integration tab.")

if len(sys.argv) < 2:
    sys.exit("Usage: python3 send_alert.py <path to an alert file>")
path = Path(sys.argv[1])

if path.suffix == ".txt":
    response = requests.post(url, data=path.read_text().strip(), headers={"Content-Type": "text/plain"}, timeout=10)
else:
    response = requests.post(url, json=json.loads(path.read_text()), timeout=10)

if response.status_code == 429:
    sys.exit(f"Rate limited. Wait {response.headers.get('Retry-After', 'a moment')} seconds, then resend.")

try:
    body = response.json()
except ValueError:
    body = {"raw": response.text}

print(response.status_code, json.dumps(body))
if not response.ok or body.get("status") != "processed":
    sys.exit(1)
