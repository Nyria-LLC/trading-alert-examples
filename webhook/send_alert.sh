#!/usr/bin/env bash
# Post one alert body to a Nyria strategy webhook with curl.
#
#   export NYRIA_WEBHOOK_URL='https://trades.nyria.io/webhooks/<your-strategy-token>'
#   ./send_alert.sh                              # payloads/stock-open-long.json
#   ./send_alert.sh payloads/stock-close-long.json
#
# The token in the URL is the only authentication, so keep the URL out of the repo and the
# shell history. Needs curl 7.76 or newer for --fail-with-body.
set -euo pipefail

: "${NYRIA_WEBHOOK_URL:?set NYRIA_WEBHOOK_URL to the webhook URL from the Integration tab of your strategy}"

payload="${1:-$(dirname "$0")/payloads/stock-open-long.json}"

curl --silent --show-error --fail-with-body --max-time 10 \
  --header "Content-Type: application/json" \
  --data @"$payload" \
  "$NYRIA_WEBHOOK_URL"
echo
