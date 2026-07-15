#!/usr/bin/env bash
set -euo pipefail

# Install the single entry point workers use for heavy Lean builds. The
# mission-scoped REMOTE_BUILD_COMMAND is injected by sandboxed.sh; no token or
# endpoint is persisted in this image fragment.
install -m 0755 /dev/stdin /usr/local/bin/lean-slot <<'LEAN_SLOT'
#!/bin/sh
set -u

_remote_fleet_eligible() {
  [ "${1:-}" = "lake" ] || return 1
  [ "${2:-}" = "build" ] || return 1
  [ -n "${REMOTE_BUILD_COMMAND:-}" ] || return 1
  [ -x "${REMOTE_BUILD_COMMAND}" ] || return 1
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 1
}

if _remote_fleet_eligible "$@"; then
  "${REMOTE_BUILD_COMMAND}" "$@"
  rc=$?
  case "$rc" in
    2|75)
      echo "lean-slot: remote fleet unavailable or checkout dirty (rc=$rc); using bounded local slot" >&2
      ;;
    *) exit "$rc" ;;
  esac
fi

for i in 0 1; do
  exec 9>"/tmp/lean-slot-$i.lock"
  if flock -n 9; then exec "$@"; fi
  exec 9>&-
done
exec 9>"/tmp/lean-slot-0.lock"
flock -w 2700 9 || {
  echo "lean-slot: no local slot after 45min" >&2
  exit 75
}
exec "$@"
LEAN_SLOT

/usr/local/bin/lean-slot true
