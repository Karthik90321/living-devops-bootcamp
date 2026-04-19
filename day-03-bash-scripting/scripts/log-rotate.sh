#!/bin/bash
# log-rotate.sh — compress and rotate a log file
# Usage: ./log-rotate.sh <path-to-log-file>
# Exit codes: 0 = success, 1 = missing arg, 2 = file not found, 3 = compression failed

LOG_FILE="$1"

# Validate input
if [ -z "$LOG_FILE" ]; then
    echo "ERROR: No log file specified" >&2
    echo "Usage: $0 <path-to-log-file>" >&2
    exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
    echo "ERROR: Log file '$LOG_FILE' does not exist" >&2
    exit 2
fi

# Build timestamp + archive name
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_NAME="${LOG_FILE}.${TIMESTAMP}.gz"

echo "Rotating: $LOG_FILE"
echo "Archive: $ARCHIVE_NAME"

# Compress (gzip -c writes to stdout, > redirects to file, original stays)
gzip -c "$LOG_FILE" > "$ARCHIVE_NAME"
if [ $? -ne 0 ]; then
    echo "ERROR: Compression failed" >&2
    exit 3
fi

# Truncate the original (keep the file, empty its contents)
> "$LOG_FILE"

echo "SUCCESS: Original truncated, archive created"
echo "Archive size: $(ls -lh $ARCHIVE_NAME | awk '{print $5}')"
exit 0
EOF
