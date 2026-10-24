#!/usr/bin/env bash
# Post one alert body to a Nyria strategy webhook with curl.
#
#   export NYRIA_WEBHOOK_URL='https://trades.nyria.io/webhooks/<your-strategy-token>'
#   ./send_alert.sh schwab/stock-open-long.json
#   ./send_alert.sh alpaca/plain-text.txt
#
# A .txt file goes as text/plain and anything else as application/json. The token in the URL
# is the only authentication, so keep the URL out of the repo and the shell history. Needs
# curl 7.76 or newer for --fail-with-body.
set -euo pipefail

: "${NYRIA_WEBHOOK_URL:?set NYRIA_WEBHOOK_URL to the webhook URL from the Integration tab of your strategy}"
: "${1:?usage: send_alert.sh <path to an alert file>}"

payload="$1"
case "$payload" in
  *.txt) content_type="text/plain" ;;
  *) content_type="application/json" ;;
esac

curl --silent --show-error --fail-with-body --max-time 10 \
  --header "Content-Type: $content_type" \
  --data-binary @"$payload" \
  "$NYRIA_WEBHOOK_URL"
echo
