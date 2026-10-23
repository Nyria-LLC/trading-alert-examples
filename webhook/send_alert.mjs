// Post one alert body to a Nyria strategy webhook with fetch (Node 18 or newer).
//
//   export NYRIA_WEBHOOK_URL='https://trades.nyria.io/webhooks/<your-strategy-token>'
//   node send_alert.mjs                              # payloads/stock-open-long.json
//   node send_alert.mjs payloads/stock-close-long.json
//
// Exit status is 0 only when Nyria answers {"status": "processed"}. A 200 can also carry a
// rejection or a duplicate, so the body is checked as well as the status code. A 200 means the
// alert was read and handed to the bots on the strategy; it does not mean the broker filled it.
import { readFile } from "node:fs/promises"

const url = process.env.NYRIA_WEBHOOK_URL
if (!url) {
  console.error("Set NYRIA_WEBHOOK_URL to the webhook URL from the strategy's Integration tab.")
  process.exit(2)
}

const path = process.argv[2] ?? new URL("./payloads/stock-open-long.json", import.meta.url)
const payload = JSON.parse(await readFile(path, "utf8"))

const response = await fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload),
  signal: AbortSignal.timeout(10_000),
})

if (response.status === 429) {
  console.error(`Rate limited. Wait ${response.headers.get("Retry-After") ?? "a moment"} seconds, then resend.`)
  process.exit(1)
}

const text = await response.text()
let body
try {
  body = JSON.parse(text)
} catch {
  body = { raw: text }
}

console.log(response.status, JSON.stringify(body))
if (!response.ok || body.status !== "processed") process.exit(1)
