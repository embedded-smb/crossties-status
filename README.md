# Crosstie status

The public status page for Crosstie, at status.crossties.pro. It runs on GitHub Pages, separate from Crosstie's own hosting, so it stays up when Crosstie is down (NFR-16).

- `.github/workflows/monitor.yml` checks each component in `targets.json` about every 5 minutes and commits `status.json` and the daily tallies in `history.json`.
- `incidents.json` holds planned maintenance and incident notes, edited by hand.
- Until Crosstie launches, `targets.json` has `"launched": false`; the page says so, and the monitor checks nothing. Set it to `true` once crossties.pro is live.

The uptime goal is 99.5% a month. Maintenance announced more than 3 days ahead doesn't count against it.
