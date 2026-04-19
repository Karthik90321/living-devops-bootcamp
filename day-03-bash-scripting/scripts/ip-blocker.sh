#!/bin/bash
# ip-blocker.sh — flag IPs exceeding access threshold
# Usage: ./ip-blocker.sh <ip-list-file> <log-file> [threshold]
# Exit codes: 0 = success, 1 = bad args, 2 = file missing

IP_LIST="$1"
LOG_FILE="$2"
THRESHOLD="${3:-10}"   # default to 10 if not given

# Validate
if [ -z "$IP_LIST" ] || [ -z "$LOG_FILE" ]; then
    echo "Usage: $0 <ip-list-file> <log-file> [threshold]" >&2
    exit 1
fi

if [ ! -f "$IP_LIST" ]; then
    echo "ERROR: IP list file '$IP_LIST' not found" >&2
    exit 2
fi

if [ ! -f "$LOG_FILE" ]; then
    echo "ERROR: Log file '$LOG_FILE' not found" >&2
    exit 2
fi

echo "================================="
echo " IP Threat Scan"
echo " IP list:   $IP_LIST"
echo " Log file:  $LOG_FILE"
echo " Threshold: $THRESHOLD hits"
echo "================================="

# Loop through each IP in the blocklist
for ip in $(cat "$IP_LIST"); do
    occurrence=$(grep -c "$ip" "$LOG_FILE")

    if [ "$occurrence" -gt "$THRESHOLD" ]; then
        echo "[BLOCK] $ip — $occurrence hits (exceeds $THRESHOLD)"
        # In production this would call: iptables, fail2ban, or send a Slack alert
    elif [ "$occurrence" -gt 0 ]; then
        echo "[WATCH] $ip — $occurrence hits (under threshold)"
    else
        echo "[OK]    $ip — no hits"
    fi
done

echo "================================="
echo "Scan complete."
exit 0
