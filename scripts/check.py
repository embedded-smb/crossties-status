"""Checks each component once, then updates status.json and the daily tallies in history.json.

Runs from the scheduled workflow. Uses only the standard library, so the runner needs nothing installed.
"""
import json
import urllib.request
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
targets = json.load(open("targets.json"))
history = json.load(open("history.json"))
results = []
if not targets.get("launched"):
    # Nothing to check before launch, and nothing to commit.
    raise SystemExit(0)
if targets.get("launched"):
    for component in targets["components"]:
        ok = False
        try:
            with urllib.request.urlopen(component["url"], timeout=10) as response:
                ok = 200 <= response.status < 300
        except Exception:  # Any failure to answer counts as down.
            ok = False
        results.append({"name": component["name"], "ok": ok})
        day = history["days"].setdefault(now.date().isoformat(), {})
        tally = day.setdefault(component["name"], {"checks": 0, "up": 0})
        tally["checks"] += 1
        tally["up"] += 1 if ok else 0

# Keep 90 days.
cutoff = (now - timedelta(days=90)).date().isoformat()
history["days"] = {d: v for d, v in history["days"].items() if d >= cutoff}
json.dump({"checkedAt": now.isoformat(timespec="seconds"), "launched": bool(targets.get("launched")), "components": results}, open("status.json", "w"), indent=2)
json.dump(history, open("history.json", "w"), indent=2, sort_keys=True)
